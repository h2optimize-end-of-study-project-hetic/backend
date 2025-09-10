"""avoid_overlaps_roomtag

Revision ID: ca4798a67204
Revises: f743ab8a8305
Create Date: 2025-09-07 13:39:26.140250

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'ca4798a67204'
down_revision: Union[str, Sequence[str], None] = 'f743ab8a8305'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        """
        CREATE OR REPLACE FUNCTION check_room_tag_overlap()
        RETURNS TRIGGER AS $$
        BEGIN
          IF EXISTS (
            SELECT 1
            FROM room_tag rt
                WHERE rt.tag_id = NEW.tag_id
                  AND rt.id <> COALESCE(NEW.id, -1)
                  AND (
                    (rt.end_at IS NULL OR NEW.start_at <= rt.end_at)
                    AND (NEW.end_at IS NULL OR rt.start_at <= NEW.end_at)
                  )
          ) THEN
            RAISE EXCEPTION 'Already exist';
          END IF;

          RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;

        CREATE TRIGGER room_tag_no_overlap
        BEFORE INSERT OR UPDATE ON room_tag
        FOR EACH ROW EXECUTE FUNCTION check_room_tag_overlap();
        """
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(
        """
        DROP TRIGGER IF EXISTS room_tag_no_overlap ON room_tag;
        DROP FUNCTION IF EXISTS check_room_tag_overlap;
        """
    )
