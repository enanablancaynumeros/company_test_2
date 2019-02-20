"""Change this

Revision ID: 00
Revises: 
Create Date: 2019-02-19 15:47:53.083149

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "00"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "stations",
        sa.Column("station_id", sa.String(), nullable=False),
        sa.Column("from_date", sa.Date(), nullable=True),
        sa.Column("to_date", sa.Date(), nullable=True),
        sa.Column("stations_hoehe", sa.String(), nullable=True),
        sa.Column("latitude", sa.Float(), nullable=True),
        sa.Column("longitude", sa.Float(), nullable=True),
        sa.Column("station_name", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("station_id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("stations")
    # ### end Alembic commands ###
