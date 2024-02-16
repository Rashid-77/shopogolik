'''
    The limited version of user crud from auth service.
    It does not save hashed password
'''
from typing import Any, Dict, Optional, Union

from sqlalchemy import or_
from sqlalchemy.orm import Session

from crud.base import CRUDBase
from models.user_lim import User
from schemas.user_lim import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_username(self, db: Session, *, username: str) -> Optional[User]:
        return db.query(User).filter(User.username == username).first()

    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()
    
    def get_by_user_id(self, db: Session, user_id: int) -> Optional[User]:
        return db.query(User).filter(User.user_id == user_id).first()
    
    def is_user_exists(self, db: Session, username: str, email: str) -> Optional[User]:
        return db.query(User) \
                    .filter(or_(User.username == username, User.email == email)) \
                    .first()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        db_obj = User(
            username=obj_in.username,
            first_name=obj_in.first_name,
            last_name=obj_in.last_name,
            email = obj_in.email,
            phone = obj_in.phone,
            disabled=False,
            is_superuser=obj_in.is_superuser,
            user_id = obj_in.user_id
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def is_active(self, user: User) -> bool:
        return not user.disabled


user = CRUDUser(User)
