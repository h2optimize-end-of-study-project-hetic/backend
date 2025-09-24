import logging
from datetime import datetime, timedelta
from typing import Any
from statistics import mean

from sqlmodel import Session, select

from app.src.domain.interface_repositories.data_repository import DataRepository

from app.src.infrastructure.db.models.room_model import RoomModel
from app.src.infrastructure.db.models.room_tag_model import RoomTagModel
from app.src.infrastructure.db.models.sensor_model import SensorHumidityModel, SensorPressureModel, SensorTemperatureModel
from app.src.infrastructure.db.models.tag_model import TagModel

logger = logging.getLogger(__name__)


class SQLDataRepository(DataRepository):
    def __init__(self, session_app: Session, session_recorded: Session):
        self.session_app = session_app
        self.session_recorded = session_recorded

    def get_rooms_with_sensor_data(
        self,
        room_ids: list[int] | None = None,
        first_value_date: datetime | None = None,
        smooth_interval_minutes: int = 30
    ) -> list[dict[str, Any]]:
        try:
            statement = (
                select(RoomModel, TagModel, RoomTagModel)
                .join(RoomTagModel, RoomModel.id == RoomTagModel.room_id)
                .join(TagModel, TagModel.id == RoomTagModel.tag_id)
            )

            if room_ids:
                statement = statement.where(RoomModel.id.in_(room_ids))

            if first_value_date:
                statement = statement.where(
                    (RoomTagModel.start_at <= first_value_date) &
                    ((RoomTagModel.end_at.is_(None)) | (RoomTagModel.end_at >= first_value_date))
                )

            results = self.session_app.exec(statement).all()
            
            rooms_data = {}
            for room, tag, room_tag in results:
                room_id = room.id
                if room_id not in rooms_data:
                    rooms_data[room_id] = {
                        "room": room,
                        "tags": [],
                        "source_addresses": []
                    }
                
                rooms_data[room_id]["tags"].append({
                    "id": room_tag.id,
                    "tag": tag,
                    "start_at": room_tag.start_at,
                    "end_at": room_tag.end_at,
                    "created_at": room_tag.created_at,
                    "updated_at": room_tag.updated_at
                })
                rooms_data[room_id]["source_addresses"].append(tag.source_address)

            result = []
            for room_id, room_info in rooms_data.items():
                room_sensor_data = self._get_room_sensor_data(
                    room_info["source_addresses"],
                    first_value_date,
                    smooth_interval_minutes
                )

                result.append({
                    **room_info["room"].model_dump(),
                    "tags": room_info["tags"],
                    **room_sensor_data
                })

            return result

        except Exception as e:
            logger.error(f"Erreur lors de la récupération des données: {e}")
            raise

    def _get_room_sensor_data(
        self,
        source_addresses: list[str],
        first_value_date: datetime | None,
        smooth_interval_minutes: int
    ) -> dict[str, Any]:

        result = {}

        temp_data = self._get_sensor_type_data(
            SensorTemperatureModel, 
            "temperature", 
            source_addresses, 
            first_value_date, 
            smooth_interval_minutes
        )
        if temp_data:
            result["temperature"] = temp_data

        humidity_data = self._get_sensor_type_data(
            SensorHumidityModel, 
            "humidity", 
            source_addresses, 
            first_value_date, 
            smooth_interval_minutes
        )
        if humidity_data:
            result["humidity"] = humidity_data

        pressure_data = self._get_sensor_type_data(
            SensorPressureModel, 
            "atmospheric_pressure", 
            source_addresses, 
            first_value_date, 
            smooth_interval_minutes
        )
        if pressure_data:
            result["pressure"] = pressure_data

        return result

    def _get_sensor_type_data(
        self,
        model_class,
        value_field: str,
        source_addresses: list[str],
        first_value_date: datetime | None,
        smooth_interval_minutes: int
    ) -> dict[str, Any] | None:
        try:
            statement = select(model_class).where(
                model_class.source_address.in_(source_addresses)
            )

            if first_value_date:
                statement = statement.where(model_class.time >= first_value_date)

            statement = statement.order_by(model_class.time)
            raw_data = self.session_recorded.exec(statement).all()

            if not raw_data:
                return None

            all_values = []
            data_by_source = {}

            for record in raw_data:
                value = getattr(record, value_field)
                if value is not None:
                    all_values.append(value)
                    
                    source = record.source_address
                    if source not in data_by_source:
                        data_by_source[source] = []
                    
                    data_by_source[source].append({
                        "time": record.time,
                        "value": value
                    })

            if not all_values:
                return None

            stats = {
                "min": min(all_values),
                "max": max(all_values),
                "average": round(mean(all_values), 2),
                "nombre_values": len(all_values)
            }

            smoothed_data = self._smooth_and_aggregate_data(
                data_by_source, 
                smooth_interval_minutes
            )

            data_points = [
                [int(point["time"].timestamp() * 1000), point["value"]]
                for point in smoothed_data
            ]

            return {
                **stats,
                "data": data_points
            }

        except Exception as e:
            logger.error(f"Erreur lors du traitement des données {value_field}: {e}")
            return None

    def _smooth_and_aggregate_data(
        self,
        data_by_source: dict[str, list[dict]],
        interval_minutes: int
    ) -> list[dict]:
        if not data_by_source:
            return []

        all_times = []
        for source_data in data_by_source.values():
            all_times.extend([point["time"] for point in source_data])
        
        if not all_times:
            return []

        min_time = min(all_times)
        max_time = max(all_times)

        interval_delta = timedelta(minutes=interval_minutes)
        time_points = []
        current_time = min_time
        
        minutes_offset = current_time.minute % interval_minutes
        if minutes_offset != 0:
            current_time = current_time.replace(
                minute=current_time.minute - minutes_offset, 
                second=0, 
                microsecond=0
            )
            current_time += interval_delta
        
        while current_time <= max_time:
            time_points.append(current_time)
            current_time += interval_delta

        smoothed_by_source = {}
        for source, source_data in data_by_source.items():
            smoothed_by_source[source] = self._interpolate_data(source_data, time_points)

        aggregated_data = []
        for time_point in time_points:
            values_at_time = []
            
            for source in smoothed_by_source:
                for point in smoothed_by_source[source]:
                    if point["time"] == time_point and point["value"] is not None:
                        values_at_time.append(point["value"])
                        break

            if values_at_time:
                avg_value = mean(values_at_time)
                aggregated_data.append({
                    "time": time_point,
                    "value": round(avg_value, 2)
                })

        return aggregated_data

    def _interpolate_data(
        self,
        source_data: list[dict],
        time_points: list[datetime]
    ) -> list[dict]:
        """
        Interpole les données manquantes pour une source
        """
        if not source_data:
            return [{"time": tp, "value": None} for tp in time_points]

        source_data.sort(key=lambda x: x["time"])
        
        interpolated = []
        
        for time_point in time_points:
            before_point = None
            after_point = None
            exact_match = None
            
            for data_point in source_data:
                if data_point["time"] == time_point:
                    exact_match = data_point
                    break
                elif data_point["time"] < time_point:
                    before_point = data_point
                elif data_point["time"] > time_point:
                    after_point = data_point
                    break

            if exact_match:
                interpolated.append({
                    "time": time_point,
                    "value": exact_match["value"]
                })
                continue

            if before_point and after_point:
                time_diff = (after_point["time"] - before_point["time"]).total_seconds()
                target_diff = (time_point - before_point["time"]).total_seconds()
                
                if time_diff > 0:
                    ratio = target_diff / time_diff
                    interpolated_value = (
                        before_point["value"] + 
                        ratio * (after_point["value"] - before_point["value"])
                    )
                    interpolated.append({
                        "time": time_point,
                        "value": round(interpolated_value, 2)
                    })
                else:
                    interpolated.append({
                        "time": time_point,
                        "value": before_point["value"]
                    })
            
            elif before_point and not after_point:
                interpolated.append({
                    "time": time_point,
                    "value": before_point["value"]
                })
            
            elif after_point and not before_point:
                interpolated.append({
                    "time": time_point,
                    "value": after_point["value"]
                })
            
            else:
                interpolated.append({
                    "time": time_point,
                    "value": None
                })

        return interpolated