"""create initial superuser

Revision ID: 003_create_initial_superuser
Revises: 002_add_contacts
Create Date: 2025-02-02 23:15:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.security import get_password_hash
import logging

# revision identifiers, used by Alembic.
revision = '003_create_initial_superuser'
down_revision = '002_add_contacts'
branch_labels = None
depends_on = None

log = logging.getLogger("alembic.runtime.migration")

def upgrade() -> None:
    # Get database connection
    connection = op.get_bind()
    session = Session(bind=connection)
    
    try:
        # Log the values we're using (for debugging)
        log.info(f"Creating superuser with email: {settings.INITIAL_SUPERUSER_EMAIL}")
        
        # Create superuser
        hashed_password = get_password_hash(settings.INITIAL_SUPERUSER_PASSWORD)
        
        # Insert superuser
        session.execute(
            sa.text("""
            INSERT INTO t_user (email, full_name, hashed_password, is_active, is_superuser)
            VALUES (:email, 'System Admin', :hashed_password, true, true)
            """),
            {
                'email': str(settings.INITIAL_SUPERUSER_EMAIL),
                'hashed_password': hashed_password
            }
        )
        
        session.commit()
        log.info("Superuser created successfully!")
    
    except Exception as e:
        log.error(f"Error creating superuser: {str(e)}")
        session.rollback()
        raise
    finally:
        session.close()

def downgrade() -> None:
    connection = op.get_bind()
    session = Session(bind=connection)
    
    try:
        # Remove the superuser
        session.execute(
            sa.text("""
            DELETE FROM t_user
            WHERE email = :email AND is_superuser = true
            """),
            {'email': str(settings.INITIAL_SUPERUSER_EMAIL)}
        )
        
        session.commit()
    except Exception as e:
        session.rollback()
        raise
    finally:
        session.close()