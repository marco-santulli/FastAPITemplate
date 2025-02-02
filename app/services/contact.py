import logging
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.contact import Contact
from app.schemas.contact import ContactCreate, ContactUpdate

log = logging.getLogger(__name__)

def get_contact(db: Session, user_id: int, contact_id: int) -> Optional[Contact]:
    """Get contact by ID, ensuring it belongs to the user."""
    return db.query(Contact).filter(
        Contact.id == contact_id,
        Contact.user_id == user_id
    ).first()

def get_user_contacts(
    db: Session,
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None
) -> List[Contact]:
    """Get all contacts for a user with optional search."""
    query = db.query(Contact).filter(Contact.user_id == user_id)
    
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                Contact.first_name.ilike(search_term),
                Contact.last_name.ilike(search_term),
                Contact.email.ilike(search_term),
                Contact.phone.ilike(search_term)
            )
        )
    
    return query.offset(skip).limit(limit).all()

def create_contact(
    db: Session,
    user_id: int,
    contact_in: ContactCreate
) -> Contact:
    """Create new contact."""
    db_contact = Contact(
        user_id=user_id,
        **contact_in.model_dump()
    )
    db.add(db_contact)
    try:
        db.commit()
        db.refresh(db_contact)
        log.info(f"Created contact {db_contact.id} for user {user_id}")
        return db_contact
    except Exception as e:
        log.error(f"Error creating contact: {str(e)}")
        db.rollback()
        raise

def update_contact(
    db: Session,
    contact: Contact,
    contact_in: ContactUpdate
) -> Contact:
    """Update contact details."""
    update_data = contact_in.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(contact, field, value)

    try:
        db.commit()
        db.refresh(contact)
        log.info(f"Updated contact {contact.id}")
        return contact
    except Exception as e:
        log.error(f"Error updating contact: {str(e)}")
        db.rollback()
        raise

def delete_contact(db: Session, contact: Contact) -> bool:
    """Delete contact."""
    try:
        db.delete(contact)
        db.commit()
        log.info(f"Deleted contact {contact.id}")
        return True
    except Exception as e:
        log.error(f"Error deleting contact: {str(e)}")
        db.rollback()
        raise

def get_total_contacts(db: Session, user_id: int, search: Optional[str] = None) -> int:
    """Get total number of contacts for a user with optional search."""
    query = db.query(Contact).filter(Contact.user_id == user_id)
    
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                Contact.first_name.ilike(search_term),
                Contact.last_name.ilike(search_term),
                Contact.email.ilike(search_term),
                Contact.phone.ilike(search_term)
            )
        )
    
    return query.count()
