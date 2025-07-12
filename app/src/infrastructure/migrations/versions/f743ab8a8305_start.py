"""Initial migration

Revision ID: f743ab8a8305
Revises: 
Create Date: 2025-07-12 06:36:57.197013
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = 'f743ab8a8305'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.execute("""
    CREATE OR REPLACE FUNCTION set_updated_at()
    RETURNS TRIGGER AS $$
    BEGIN
      NEW.updated_at = NOW();
      RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
    """)

    op.execute("""
    CREATE OR REPLACE FUNCTION update_room_count()
    RETURNS TRIGGER AS $$
    BEGIN
      UPDATE building
      SET room_count = (
        SELECT COUNT(*) FROM room WHERE building_id = NEW.building_id
      )
      WHERE id = NEW.building_id;
      RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
    """)

    op.execute("""
    CREATE OR REPLACE FUNCTION auto_finish_event_room()
    RETURNS TRIGGER AS $$
    BEGIN
      IF NEW.end_at < NOW() THEN
        NEW.is_finished := TRUE;
      END IF;
      RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
    """)

    op.execute("""
    CREATE OR REPLACE FUNCTION set_deleted_at()
    RETURNS TRIGGER AS $$
    BEGIN
      IF NEW.is_delete = TRUE AND OLD.is_delete = FALSE THEN
        NEW.deleted_at := NOW();
      ELSIF NEW.is_delete = FALSE THEN
        NEW.deleted_at := NULL;
      END IF;
      RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
    """)

    op.create_table(
        'building',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.Text),
        sa.Column('description', sa.Text),
        sa.Column('room_count', sa.Integer),
        sa.Column('street_number', sa.Text),
        sa.Column('street_name', sa.Text),
        sa.Column('postal_code', sa.Text),
        sa.Column('city', sa.Text),
        sa.Column('country', sa.Text),
        sa.Column('latitude', sa.Numeric(9, 6)),
        sa.Column('longitude', sa.Numeric(9, 6)),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True))
    )

    op.create_table(
        'tag',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.Text),
        sa.Column('description', sa.Text),
        sa.Column('source_address', sa.Text, unique=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True))
    )

    op.create_table(
        'map',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('building_id', sa.Integer, sa.ForeignKey('building.id')),
        sa.Column('file_name', sa.Text),
        sa.Column('path', sa.Text),
        sa.Column('width', sa.Integer),
        sa.Column('length', sa.Integer),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True))
    )

    op.create_table(
        'room',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.Text),
        sa.Column('description', sa.Text),
        sa.Column('floor', sa.Integer),
        sa.Column('building_id', sa.Integer, sa.ForeignKey('building.id')),
        sa.Column('area', sa.Float),
        sa.Column('shape', postgresql.JSONB),
        sa.Column('capacity', sa.Integer),
        sa.Column('start_at', sa.TIMESTAMP(timezone=True)),
        sa.Column('end_at', sa.TIMESTAMP(timezone=True)),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True)),
        sa.CheckConstraint('end_at IS NULL OR start_at IS NULL OR end_at > start_at')
    )

    op.create_table(
        'user',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('email', sa.Text, unique=True, nullable=False),
        sa.Column('salt', sa.Text, nullable=False),
        sa.Column('password', sa.Text, nullable=False),
        sa.Column('secret_2fa', sa.Text),
        sa.Column('role', sa.Enum('admin', 'staff', 'technician', 'intern', 'guest', name='role'), server_default='guest'),
        sa.Column('firstname', sa.Text, nullable=False),
        sa.Column('lastname', sa.Text, nullable=False),
        sa.Column('phone_number', sa.Text),
        sa.Column('is_active', sa.Boolean, server_default=sa.text('TRUE')),
        sa.Column('is_delete', sa.Boolean, server_default=sa.text('FALSE')),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True)),
        sa.Column('deleted_at', sa.TIMESTAMP(timezone=True))
    )

    op.create_table(
        'group',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.Text),
        sa.Column('description', sa.Text),
        sa.Column('member_count', sa.Integer),
        sa.Column('start_at', sa.TIMESTAMP(timezone=True)),
        sa.Column('end_at', sa.TIMESTAMP(timezone=True)),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True)),
        sa.CheckConstraint('end_at IS NULL OR start_at IS NULL OR end_at > start_at')
    )

    op.create_table(
        'event',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.Text),
        sa.Column('description', sa.Text),
        sa.Column('group_id', sa.Integer, sa.ForeignKey('group.id')),
        sa.Column('supervisor', sa.Text),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True))
    )

    op.create_table(
        'event_room',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('room_id', sa.Integer, sa.ForeignKey('room.id')),
        sa.Column('event_id', sa.Integer, sa.ForeignKey('event.id')),
        sa.Column('is_finished', sa.Boolean, server_default=sa.text('FALSE')),
        sa.Column('start_at', sa.TIMESTAMP(timezone=True)),
        sa.Column('end_at', sa.TIMESTAMP(timezone=True)),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True)),
        sa.CheckConstraint('end_at IS NULL OR start_at IS NULL OR end_at > start_at'),
        sa.UniqueConstraint('event_id', 'room_id', 'start_at', 'end_at')
    )

    op.create_table(
        'room_tag',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('tag_id', sa.Integer, sa.ForeignKey('tag.id')),
        sa.Column('room_id', sa.Integer, sa.ForeignKey('room.id')),
        sa.Column('start_at', sa.TIMESTAMP(timezone=True)),
        sa.Column('end_at', sa.TIMESTAMP(timezone=True)),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True)),
        sa.CheckConstraint('end_at IS NULL OR start_at IS NULL OR end_at > start_at')
    )

    op.create_table(
        'user_group',
        sa.Column('group_id', sa.Integer, sa.ForeignKey('group.id'), primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('user.id'), primary_key=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True))
    )

    for table in ["user", "building", "map", "room", "group", "user_group", "event", "tag", "room_tag", "event_room"]:
        op.execute(f"""
        CREATE TRIGGER trg_{table}_updated_at
        BEFORE UPDATE ON "{table}"
        FOR EACH ROW
        EXECUTE FUNCTION set_updated_at();
        """)

    op.execute("""
    CREATE TRIGGER trg_room_after_insert
    AFTER INSERT ON room
    FOR EACH ROW
    EXECUTE FUNCTION update_room_count();
    """)
    op.execute("""
    CREATE TRIGGER trg_room_after_delete
    AFTER DELETE ON room
    FOR EACH ROW
    EXECUTE FUNCTION update_room_count();
    """)
    op.execute("""
    CREATE TRIGGER trg_room_after_update
    AFTER UPDATE ON room
    FOR EACH ROW
    WHEN (OLD.building_id IS DISTINCT FROM NEW.building_id)
    EXECUTE FUNCTION update_room_count();
    """)

    op.execute("""
    CREATE TRIGGER trg_auto_finish_event_room
    BEFORE INSERT OR UPDATE ON event_room
    FOR EACH ROW
    EXECUTE FUNCTION auto_finish_event_room();
    """)

    op.execute("""
    CREATE TRIGGER trg_user_soft_delete
    BEFORE UPDATE ON "user"
    FOR EACH ROW
    EXECUTE FUNCTION set_deleted_at();
    """)


def downgrade() -> None:
    for table in ["user", "building", "map", "room", "group", "user_group", "event", "tag", "room_tag", "event_room"]:
        op.execute(f'DROP TRIGGER IF EXISTS trg_{table}_updated_at ON "{table}";')
    op.execute("DROP TRIGGER IF EXISTS trg_room_after_insert ON room;")
    op.execute("DROP TRIGGER IF EXISTS trg_room_after_delete ON room;")
    op.execute("DROP TRIGGER IF EXISTS trg_room_after_update ON room;")
    op.execute("DROP TRIGGER IF EXISTS trg_auto_finish_event_room ON event_room;")
    op.execute("DROP TRIGGER IF EXISTS trg_user_soft_delete ON \"user\";")

    op.execute("DROP FUNCTION IF EXISTS set_updated_at;")
    op.execute("DROP FUNCTION IF EXISTS update_room_count;")
    op.execute("DROP FUNCTION IF EXISTS auto_finish_event_room;")
    op.execute("DROP FUNCTION IF EXISTS set_deleted_at;")

    for table in reversed([
        'user_group', 'event_room', 'room_tag', 'event', 'group',
        'user', 'room', 'map', 'tag', 'building'
    ]):
        op.drop_table(table)

    role_enum = postgresql.ENUM('admin', 'staff', 'technician', 'intern', 'guest', name='role')
    role_enum.drop(op.get_bind(), checkfirst=True)
