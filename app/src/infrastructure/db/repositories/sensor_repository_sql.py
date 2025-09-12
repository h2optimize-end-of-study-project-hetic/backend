from __future__ import annotations
from datetime import datetime
from typing import Any, Type

from sqlmodel import Session, select, SQLModel
from sqlalchemy import func

_TS_CANDIDATES = ("time", "recorded_at", "measured_at", "created_at", "timestamp", "ts")


class SQLSensorRepository:
    def __init__(self, session: Session, model: Type[SQLModel], ts_attr: str | None = None):
        self.session = session
        self.model = model
        self.ts_attr = ts_attr or self._detect_ts_attr()

    def _detect_ts_attr(self) -> str:
        for name in _TS_CANDIDATES:
            if hasattr(self.model, name):
                return name
        raise AttributeError(
            f"Aucune colonne temporelle trouvée dans le modèle {self.model.__name__}"
        )

    @property
    def ts_col(self):
        return getattr(self.model, self.ts_attr)


    def get_latest(self) -> Any | None:
        """Retourne la dernière mesure insérée"""
        stmt = select(self.model).order_by(self.ts_col.desc()).limit(1)
        return self.session.exec(stmt).first()

    def get_all(self, limit: int = 100) -> list[Any]:
        """Retourne les N dernières mesures"""
        stmt = select(self.model).order_by(self.ts_col.desc()).limit(limit)
        return list(self.session.exec(stmt).all())

    def get_range(self, start: datetime, end: datetime, limit: int | None = None) -> list[Any]:
        """Retourne les mesures dans un intervalle temporel"""
        stmt = (
            select(self.model)
            .where(self.ts_col >= start, self.ts_col <= end)
            .order_by(self.ts_col.desc())
        )
        if limit:
            stmt = stmt.limit(limit)
        return list(self.session.exec(stmt).all())

    def paginate(
        self, cursor_time: datetime | None, limit: int
    ) -> tuple[list[Any], int, Any | None, Any | None]:
        """
        Pagination basée sur la colonne temporelle (TimescaleDB friendly).
        """
        stmt = select(self.model)
        if cursor_time is not None:
            stmt = stmt.where(self.ts_col >= cursor_time)
        stmt = stmt.order_by(self.ts_col).limit(limit)

        rows = self.session.exec(stmt).all()

        # Compte total
        total = self.session.exec(select(func.count()).select_from(self.model)).one()
        total = total[0] if isinstance(total, tuple) else total

        first_row = rows[0] if rows else None
        last_row = rows[-1] if rows else None
        return list(rows), int(total or 0), first_row, last_row
