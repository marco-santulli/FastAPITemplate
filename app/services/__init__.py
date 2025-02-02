from app.services.user import (  # noqa
    get_user_by_id,
    get_user_by_email,
    create_user,
    update_user,
    authenticate_user,
    get_users  # Added this new function
)

from app.services.contact import (  # noqa
    get_contact,
    get_user_contacts,
    create_contact,
    update_contact,
    delete_contact,
    get_total_contacts
)

__all__ = [
    # User service functions
    "get_user_by_id",
    "get_user_by_email",
    "create_user",
    "update_user",
    "authenticate_user",
    "get_users",
    
    # Contact service functions
    "get_contact",
    "get_user_contacts",
    "create_contact",
    "update_contact",
    "delete_contact",
    "get_total_contacts"
]