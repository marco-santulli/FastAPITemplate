import logging
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.v1.endpoints.users import get_current_user
from app.models.user import User
from app.schemas.contact import Contact, ContactCreate, ContactUpdate
from app.services import contact as contact_service

log = logging.getLogger(__name__)
router = APIRouter()

@router.get("/", response_model=List[Contact])
def list_contacts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    search: Optional[str] = Query(None, min_length=1),
):
    """
    Retrieve all contacts for the current user.
    Optional search parameter will search across name, email, and phone.
    """
    contacts = contact_service.get_user_contacts(
        db=db,
        user_id=current_user.id,
        skip=skip,
        limit=limit,
        search=search
    )
    total = contact_service.get_total_contacts(
        db=db,
        user_id=current_user.id,
        search=search
    )
    return {
        "items": contacts,
        "total": total,
        "page": skip // limit + 1,
        "page_size": limit
    }

@router.post("/", response_model=Contact, status_code=201)
def create_contact(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    contact_in: ContactCreate,
):
    """Create a new contact for the current user."""
    try:
        contact = contact_service.create_contact(
            db=db,
            user_id=current_user.id,
            contact_in=contact_in
        )
        log.info(f"Created contact {contact.id} for user {current_user.id}")
        return contact
    except Exception as e:
        log.error(f"Error creating contact: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail="Error creating contact"
        )

@router.get("/{contact_id}", response_model=Contact)
def get_contact(
    contact_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get a specific contact by ID."""
    contact = contact_service.get_contact(
        db=db,
        user_id=current_user.id,
        contact_id=contact_id
    )
    if not contact:
        raise HTTPException(
            status_code=404,
            detail="Contact not found"
        )
    return contact

@router.put("/{contact_id}", response_model=Contact)
def update_contact(
    *,
    contact_id: int = Path(..., ge=1),
    contact_in: ContactUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update a contact."""
    contact = contact_service.get_contact(
        db=db,
        user_id=current_user.id,
        contact_id=contact_id
    )
    if not contact:
        raise HTTPException(
            status_code=404,
            detail="Contact not found"
        )
    
    try:
        updated_contact = contact_service.update_contact(
            db=db,
            contact=contact,
            contact_in=contact_in
        )
        log.info(f"Updated contact {contact_id}")
        return updated_contact
    except Exception as e:
        log.error(f"Error updating contact: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail="Error updating contact"
        )

@router.delete("/{contact_id}", status_code=204)
def delete_contact(
    contact_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete a contact."""
    contact = contact_service.get_contact(
        db=db,
        user_id=current_user.id,
        contact_id=contact_id
    )
    if not contact:
        raise HTTPException(
            status_code=404,
            detail="Contact not found"
        )
    
    try:
        contact_service.delete_contact(db=db, contact=contact)
        log.info(f"Deleted contact {contact_id}")
    except Exception as e:
        log.error(f"Error deleting contact: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail="Error deleting contact"
        )
