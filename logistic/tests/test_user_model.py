import random
import string

from api.deps import get_db
from crud.crud_user import user
from schemas.user import UserCreate


def rand_word(length):
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(length))


COURIER = f"courier-{rand_word(3)}"
EMAIL = f"{COURIER}@.mail.com"


class TestUser:
    def test_create_read(
        self,
        val=UserCreate(
            username=COURIER,
            first_name="b",
            last_name="c",
            email=EMAIL,
            phone="79001112233",
            password="w",
            disabled=False,
            is_superuser=True,
        ),
    ):
        u = user.create(db=next(get_db()), obj_in=val)
        user_1 = user.get(db=next(get_db()), id=u.id)

        assert user_1.id == u.id
        assert user_1.username == val.username
        assert user_1.first_name == val.first_name
        assert user_1.last_name == val.last_name
        assert user_1.email == val.email
        assert user_1.phone == val.phone
        assert user_1.hashed_password == u.hashed_password
        assert user_1.disabled == u.disabled
        assert user_1.is_superuser == val.is_superuser

        assert isinstance(u.id, int)
        assert isinstance(u.username, str)
        assert isinstance(u.first_name, str)
        assert isinstance(u.last_name, str)
        assert isinstance(u.email, str)
        assert isinstance(u.phone, str)
        assert isinstance(u.hashed_password, str)
        assert isinstance(u.disabled, bool)
        assert isinstance(u.is_superuser, bool)

    def test_update(self):
        with next(get_db()) as session:
            user_1 = user.get_by_email(db=session, email=EMAIL)
            assert user_1.first_name == "b"

            user_1a = user.update(
                db=session, db_obj=user_1, obj_in={"first_name": "b-1"}
            )
            assert user_1a.first_name == "b-1"

    def test_delete(self):
        user_1 = user.get_by_email(db=next(get_db()), email=EMAIL)
        assert user_1 is not None

        user_1 = user.remove(db=next(get_db()), id=user_1.id)
        assert user_1 is not None

        user_1 = user.get_by_email(db=next(get_db()), email=EMAIL)
        assert user_1 is None
