"""Create users, todo_lists, and todo_items tables."""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "0002_create_users_and_todo_tables"
down_revision = "0001_initial"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("username", sa.String(length=50), nullable=False),
        sa.Column("hashed_password", sa.String(length=128), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.UniqueConstraint("username"),
    )
    op.create_index(op.f("ix_users_id"), "users", ["id"])
    op.create_index(op.f("ix_users_username"), "users", ["username"])

    op.create_table(
        "todo_lists",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            onupdate=sa.func.now(),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], ondelete="CASCADE", name="fk_todo_lists_user_id"
        ),
    )
    op.create_index(op.f("ix_todo_lists_id"), "todo_lists", ["id"])
    op.create_index(op.f("ix_todo_lists_user_id"), "todo_lists", ["user_id"])

    op.create_table(
        "todo_items",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("completed", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("list_id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            onupdate=sa.func.now(),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["list_id"],
            ["todo_lists.id"],
            ondelete="CASCADE",
            name="fk_todo_items_list_id",
        ),
    )
    op.create_index(op.f("ix_todo_items_id"), "todo_items", ["id"])
    op.create_index(op.f("ix_todo_items_list_id"), "todo_items", ["list_id"])


def downgrade() -> None:
    op.drop_index(op.f("ix_todo_items_list_id"), table_name="todo_items")
    op.drop_index(op.f("ix_todo_items_id"), table_name="todo_items")
    op.drop_table("todo_items")

    op.drop_index(op.f("ix_todo_lists_user_id"), table_name="todo_lists")
    op.drop_index(op.f("ix_todo_lists_id"), table_name="todo_lists")
    op.drop_table("todo_lists")

    op.drop_index(op.f("ix_users_username"), table_name="users")
    op.drop_index(op.f("ix_users_id"), table_name="users")
    op.drop_table("users")
