"""init

Revision ID: 9bc40ac7fbb5
Revises:
Create Date: 2023-10-27 13:28:20.741363

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "9bc40ac7fbb5"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Preprocess
    pre_upgrade()

    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "translations",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("word", sa.String(), nullable=False),
        sa.Column("translated_word", sa.String(), nullable=False),
        sa.Column("pronunciation", sa.String(), nullable=True),
        sa.Column("source_lang", sa.String(), nullable=True),
        sa.Column("target_lang", sa.String(), nullable=False),
        sa.Column("extra_data", postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_translations_translated_word"),
        "translations",
        ["translated_word"],
        unique=False,
    )
    op.create_index(op.f("ix_translations_word"), "translations", ["word"], unique=True)
    # ### end Alembic commands ###

    # Postprocess
    post_upgrade()


def downgrade():
    # Preprocess
    pre_downgrade()

    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_translations_word"), table_name="translations")
    op.drop_index(op.f("ix_translations_translated_word"), table_name="translations")
    op.drop_table("translations")
    # ### end Alembic commands ###

    # Postprocess
    post_downgrade()


def pre_upgrade():
    # Processing before upgrading the schema
    pass


def post_upgrade():
    # Processing after upgrading the schema
    pass


def pre_downgrade():
    # Processing before downgrading the schema
    pass


def post_downgrade():
    # Processing after downgrading the schema
    pass
