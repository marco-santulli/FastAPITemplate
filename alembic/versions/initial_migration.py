"""Initial migration for creating users table."""

from alembic import op
import sqlalchemy as sa

# Revision identifiers, used by Alembic.
revision = 'initial_migration'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    """Apply the migration."""
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('email', sa.String, unique=True, index=True, nullable=False),
        sa.Column('hashed_password', sa.String, nullable=False),
    )

def downgrade():
    """Revert the migration."""
    op.drop_table('users')
