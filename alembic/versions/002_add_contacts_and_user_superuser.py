"""add contacts and user superuser

Revision ID: 002_add_contacts
Revises: 001_initial_migration
Create Date: 2025-02-02 22:30:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '002_add_contacts'
down_revision = '001_initial_migration'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Add is_superuser column to user table
    op.add_column('t_user', sa.Column('is_superuser', sa.Boolean(), nullable=False, server_default='false'))

    # Create contacts table
    op.create_table(
        't_contact',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('first_name', sa.String(), nullable=False),
        sa.Column('last_name', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=True),
        sa.Column('phone', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['t_user.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_t_contact_email'), 't_contact', ['email'], unique=False)

def downgrade() -> None:
    op.drop_index(op.f('ix_t_contact_email'), table_name='t_contact')
    op.drop_table('t_contact')
    op.drop_column('t_user', 'is_superuser')
