import uuid
from datetime import datetime

from api.deps import get_db
from crud.crud_courier import courier
from crud.crud_user import user
from schemas.courier import CourierUpdate
from schemas.user import UserCreate
from tests.test_user_model import COURIER, EMAIL


class TestCourier:
    def test_create_read(
        self,
    ):
        val = UserCreate(
            username=COURIER,
            first_name="b",
            last_name="c",
            email=EMAIL,
            phone="79001112233",
            password="w",
            disabled=False,
            is_superuser=True,
        )
        with next(get_db()) as session:
            u = user.create(session, obj_in=val)
            c = courier.create(session, user_id=u.id)
            c1 = courier.get(session, id=c.id)
            assert c.courier_id == c1.courier_id
            assert isinstance(c1.id, int)
            assert isinstance(c1.courier_id, int)
            assert isinstance(c1.from_t, datetime)
            assert isinstance(c1.to_t, datetime)
            assert isinstance(c1.order_uuid, str)
            assert isinstance(c1.deliv_addr, str)
            assert isinstance(c1.client_id, int)
            assert isinstance(c1.reserve_uuid, str)

    def test_update(self):
        with next(get_db()) as session:
            u = user.get_by_email(db=session, email=EMAIL)
            c = courier.get_courier_id(session, user_id=u.id)
            assert c.courier_id == u.id

            c_upd = CourierUpdate(
                from_t=datetime.strptime("2024-02-08 13:30:00", "%Y-%m-%d %H:%M:%S"),
                to_t=datetime.strptime("2024-02-08 18:00:00", "%Y-%m-%d %H:%M:%S"),
                order_uuid=str(uuid.uuid4()),
                deliv_addr="Common town, main street",
                client_id=1,
                reserve_uuid=str(uuid.uuid4()),
            )
            c1 = courier.update(session, db_obj=c, obj_in=c_upd)
            assert c1.order_uuid == c_upd.order_uuid
            assert c1.deliv_addr == c_upd.deliv_addr
            assert c1.client_id == c_upd.client_id
            assert c1.reserve_uuid == c_upd.reserve_uuid

    def test_delete(self):
        with next(get_db()) as session:
            u = user.get_by_email(session, email=EMAIL)
            assert u is not None

            c = courier.get_courier_id(session, user_id=u.id)
            assert c is not None

            c = courier.remove(session, user_id=u.id)
            assert u is not None

            c = courier.get_courier_id(session, user_id=u.id)
            assert c is None

            u = user.remove(session, id=u.id)
            assert u is not None

            u = user.get_by_email(session, email=EMAIL)
            assert u is None
