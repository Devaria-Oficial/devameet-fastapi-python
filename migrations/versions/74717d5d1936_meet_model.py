"""Meet model

Revision ID: 74717d5d1936
Revises: 0e924af08967
Create Date: 2023-01-29 07:30:10.756396

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '74717d5d1936'
down_revision = '0e924af08967'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('meets',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('color', sa.String(length=7), nullable=False),
    sa.Column('link', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_meets_id'), 'meets', ['id'], unique=False)
    op.create_index(op.f('ix_meets_link'), 'meets', ['link'], unique=False)
    op.create_index(op.f('ix_meets_name'), 'meets', ['name'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_meets_name'), table_name='meets')
    op.drop_index(op.f('ix_meets_link'), table_name='meets')
    op.drop_index(op.f('ix_meets_id'), table_name='meets')
    op.drop_table('meets')
    # ### end Alembic commands ###
