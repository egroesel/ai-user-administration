from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import models
import schemas
from security import get_current_admin_user
from email_service import send_test_email

router = APIRouter(prefix="/api/admin", tags=["Admin"])


@router.get("/users", response_model=List[schemas.UserResponse])
def list_users(
    skip: int = 0,
    limit: int = 100,
    current_admin: models.User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users


@router.get("/users/{user_id}", response_model=schemas.UserResponse)
def get_user(
    user_id: int,
    current_admin: models.User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.patch("/users/{user_id}", response_model=schemas.UserResponse)
def update_user(
    user_id: int,
    user_update: schemas.AdminUserUpdate,
    current_admin: models.User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user_update.is_active is not None:
        user.is_active = user_update.is_active

    if user_update.is_admin is not None:
        if user.id == current_admin.id and not user_update.is_admin:
            raise HTTPException(
                status_code=400,
                detail="Cannot remove admin privileges from yourself"
            )
        user.is_admin = user_update.is_admin

    db.commit()
    db.refresh(user)

    return user


@router.delete("/users/{user_id}", response_model=schemas.MessageResponse)
def delete_user(
    user_id: int,
    current_admin: models.User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.id == current_admin.id:
        raise HTTPException(status_code=400, detail="Cannot delete yourself")

    db.query(models.Session).filter(models.Session.user_id == user_id).delete()
    db.delete(user)
    db.commit()

    return {"message": "User deleted successfully"}


@router.post("/test-email", response_model=schemas.MessageResponse)
def send_test_email_endpoint(
    test_email_data: schemas.TestEmailRequest,
    current_admin: models.User = Depends(get_current_admin_user),
):
    """
    Send test emails for testing email functionality

    Available email types:
    - welcome: Welcome email
    - password_reset: Password reset email (with test token)
    - account_activated: Account activated notification
    - account_deactivated: Account deactivated notification
    - test_simple: Simple test email
    """

    valid_types = ["welcome", "password_reset", "account_activated", "account_deactivated", "test_simple"]

    if test_email_data.email_type not in valid_types:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid email type. Must be one of: {', '.join(valid_types)}"
        )

    success = send_test_email(
        test_email_data.email,
        test_email_data.email_type,
        test_email_data.user_name
    )

    if not success:
        raise HTTPException(
            status_code=500,
            detail="Failed to send test email. Check email service configuration."
        )

    return {"message": f"Test email '{test_email_data.email_type}' sent successfully to {test_email_data.email}"}
