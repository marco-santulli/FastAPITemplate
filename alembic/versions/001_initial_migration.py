"""initial migration

Revision ID: 001_initial_migration
Revises: 
Create Date: 2025-02-02 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '001_initial_migration'  # Changed this line
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create user table
    op.create_table(
        't_user',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('full_name', sa.String(), nullable=True),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_t_user_email'), 't_user', ['email'], unique=True)
    op.create_index(op.f('ix_t_user_id'), 't_user', ['id'], unique=False)

    # Create audit log table
    op.create_table(
        'l_user_audit',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('cod_evento', sa.String(10), nullable=False),
        sa.Column('old_data', sa.JSON(), nullable=True),
        sa.Column('new_data', sa.JSON(), nullable=True),
        sa.Column('data_aggiornamento', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('utente_aggiornamento', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.CheckConstraint("cod_evento IN ('insert', 'update', 'delete')", name='valid_event_type')
    )


def downgrade() -> None:
    op.drop_table('l_user_audit')
    op.drop_index(op.f('ix_t_user_id'), table_name='t_user')
    op.drop_index(op.f('ix_t_user_email'), table_name='t_user')
    op.drop_table('t_user')
