from sqlmodel import select, Session, func
from datetime import datetime, time, timedelta
from datetime import date as Date

from app.src.infrastructure.db.models.user_model import UserModel
from app.src.infrastructure.db.models.user_group_model import UserGroupModel
from app.src.infrastructure.db.models.group_model import GroupModel

from app.src.infrastructure.db.models.event_model import EventModel
from app.src.infrastructure.db.models.room_model import RoomModel
from app.src.infrastructure.db.models.event_room_model import EventRoomModel

class GroupUserRepository:

    def __init__(self, session: Session):
        self.session = session

    def get_group_by_id(self, group_id: int) -> GroupModel | None:
        return self.session.get(GroupModel, group_id)

    def get_users_in_group(self, group_id: int) -> list[UserModel]:
        """
        Retourne tous les utilisateurs appartenant à un groupe donné.
        """
        statement = (
            select(UserModel)
            .join(UserGroupModel, UserGroupModel.user_id == UserModel.id)
            .join(GroupModel, UserGroupModel.group_id == GroupModel.id)
            .where(GroupModel.id == group_id)
            .order_by(UserModel.firstname)
        )

        results = self.session.exec(statement).all()
        return results

# user planning

class UserEventRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_events_for_user(self, user_id: int) -> list[dict]:
        statement = (
            select(
                GroupModel.name.label("group"),
                EventModel.supervisor,
                RoomModel.name.label("room"),
                EventModel.name.label("event"),
                EventRoomModel.start_at,
                EventRoomModel.end_at,
            )
            .join(GroupModel, GroupModel.id == EventModel.group_id)
            .join(EventRoomModel, EventRoomModel.event_id == EventModel.id)
            .join(RoomModel, RoomModel.id == EventRoomModel.room_id)
            .join(UserGroupModel, UserGroupModel.group_id == GroupModel.id)
            .join(UserModel, UserModel.id == UserGroupModel.user_id)
            .where(UserModel.id == user_id)
        )

        results = self.session.exec(statement).all()
        
        # Convertir les tuples en dictionnaires
        events = []
        for row in results:
            event_dict = {
                "group": row[0],
                "supervisor": row[1],
                "room": row[2], 
                "event": row[3],
                "start_at": row[4],
                "end_at": row[5]
            }
            events.append(event_dict)
        
        return events


# events by day

class EventsByDateRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_events_by_date(self, date: Date) -> list[dict]:
        """
        Retourne tous les events d'une journée
        """
        start_of_day = datetime.combine(date, time.min)  # 2025-08-31 00:00:00
        end_of_day = datetime.combine(date, time.max)    # 2025-08-31 23:59:59.999999

        statement = (
            select(
                EventRoomModel.room_id,
                EventRoomModel.event_id,
                EventRoomModel.start_at,
                EventRoomModel.end_at,
                EventModel.supervisor,
                EventModel.name.label("event_name"),
                EventModel.description,
                EventModel.group_id,
                GroupModel.name.label("group_name"),
                GroupModel.member_count,
            )
            .join(EventModel, EventRoomModel.event_id == EventModel.id)
            .join(GroupModel, EventModel.group_id == GroupModel.id)
            .where(EventRoomModel.start_at >= start_of_day)
            .where(EventRoomModel.start_at <= end_of_day)
        )

        results = self.session.exec(statement).all()

        events = []
        for row in results:
            event_dict = {
                "room_id": row[0],
                "event_id": row[1],
                "start_at": row[2],
                "end_at": row[3],
                "supervisor": row[4],
                "event_name": row[5],
                "description": row[6],
                "group_id": row[7],
                "group_name": row[8],
                "member_count": row[9],
            }
            events.append(event_dict)

        return events