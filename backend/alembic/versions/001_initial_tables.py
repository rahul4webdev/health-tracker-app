"""Initial tables for users and food_logs

Revision ID: 001
Revises:
Create Date: 2026-01-25 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=True),
        sa.Column('age', sa.Integer(), nullable=True),
        sa.Column('gender', sa.Enum('male', 'female', 'other', name='genderenum'), nullable=True),
        sa.Column('height_cm', sa.DECIMAL(precision=5, scale=2), nullable=True),
        sa.Column('weight_kg', sa.DECIMAL(precision=5, scale=2), nullable=True),
        sa.Column('activity_level', sa.Enum('low', 'medium', 'high', name='activitylevelenum'), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)

    # Create food_logs table
    op.create_table(
        'food_logs',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('food_name', sa.String(length=255), nullable=False),
        sa.Column('calories', sa.DECIMAL(precision=7, scale=2), nullable=False),
        sa.Column('protein_g', sa.DECIMAL(precision=6, scale=2), nullable=True, default=0),
        sa.Column('carbs_g', sa.DECIMAL(precision=6, scale=2), nullable=True, default=0),
        sa.Column('fats_g', sa.DECIMAL(precision=6, scale=2), nullable=True, default=0),
        sa.Column('logged_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_food_logs_id'), 'food_logs', ['id'], unique=False)
    op.create_index('ix_food_logs_user_logged_at', 'food_logs', ['user_id', 'logged_at'], unique=False)


def downgrade() -> None:
    # Drop food_logs table
    op.drop_index('ix_food_logs_user_logged_at', table_name='food_logs')
    op.drop_index(op.f('ix_food_logs_id'), table_name='food_logs')
    op.drop_table('food_logs')

    # Drop users table
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
