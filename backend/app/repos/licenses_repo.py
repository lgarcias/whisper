from typing import Optional

from app.models import License
from sqlalchemy.orm import Session


def upsert_license(
    db: Session,
    key: str,
    plan: str,
    features: dict,
    valid_from,
    valid_until,
    is_revoked: bool = False,
    assigned_to_user_id: Optional[str] = None,
) -> License:
    """Insert or update a license by key."""
    license_obj = db.query(License).filter(License.key == key).first()
    if license_obj:
        setattr(license_obj, "plan", plan)
        setattr(license_obj, "features", features)
        setattr(license_obj, "valid_from", valid_from)
        setattr(license_obj, "valid_until", valid_until)
        setattr(license_obj, "is_revoked", is_revoked)
        setattr(license_obj, "assigned_to_user_id", assigned_to_user_id)
    else:
        license_obj = License(
            key=key,
            plan=plan,
            features=features,
            valid_from=valid_from,
            valid_until=valid_until,
            is_revoked=is_revoked,
            assigned_to_user_id=assigned_to_user_id,
        )
        db.add(license_obj)
    db.commit()
    db.refresh(license_obj)
    return license_obj


def get_license_by_key(db: Session, key: str) -> Optional[License]:
    """Retrieve a license by key."""
    return db.query(License).filter(License.key == key).first()


def assign_license_to_user(db: Session, key: str, user_id: str) -> License:
    """Assign a license to a user."""
    license_obj = db.query(License).filter(License.key == key).first()
    if not license_obj:
        raise ValueError("License not found")
    setattr(license_obj, "assigned_to_user_id", user_id)
    db.commit()
    db.refresh(license_obj)
    return license_obj
