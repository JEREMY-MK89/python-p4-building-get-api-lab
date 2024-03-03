"""Revert data type change in price column

Revision ID: 191f11f6c015
Revises: 1a660c242acb
Create Date: 2024-03-03 07:17:04.515451

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '191f11f6c015'
down_revision = '1a660c242acb'
branch_labels = None
depends_on = None

def upgrade():
    # Create a temporary table with the desired data type
    op.create_table('temp_baked_goods',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('price', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('bakery_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['bakery_id'], ['bakeries.id'], name=op.f('fk_temp_baked_goods_bakery_id_bakeries')),
        sa.PrimaryKeyConstraint('id')
    )

    # Copy data from the original table to the temporary table
    op.execute('INSERT INTO temp_baked_goods SELECT * FROM baked_goods')

    # Drop the original table
    op.drop_table('baked_goods')

    # Rename the temporary table to the original table
    op.rename_table('temp_baked_goods', 'baked_goods')

def downgrade():
    # Create a temporary table with the original data type
    op.create_table('temp_baked_goods',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('price', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('bakery_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['bakery_id'], ['bakeries.id'], name=op.f('fk_temp_baked_goods_bakery_id_bakeries')),
        sa.PrimaryKeyConstraint('id')
    )

    # Copy data from the original table to the temporary table
    op.execute('INSERT INTO temp_baked_goods SELECT * FROM baked_goods')

    # Drop the original table
    op.drop_table('baked_goods')

    # Rename the temporary table to the original table
    op.rename_table('temp_baked_goods', 'baked_goods')
