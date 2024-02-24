# import datetime
from api.deps import get_db
from crud.crud_pub_user_event import pub_user_event as event
from schemas.pub_user_event import PubUserEventCreate

USER_ID = 1


class TestPubEvent:

    def test_create_read(self, val=PubUserEventCreate(
                            user_id = USER_ID, 
                            state = "state_1", 
                            delivered = False, 
                            deliv_fail = False, 
                        )
        ):
        e = event.create(db = next(get_db()), obj_in = val)

        ev = event.get(db = next(get_db()), id=e.id)

        assert ev.user_id == val.user_id
        assert ev.state == val.state
        assert ev.delivered == val.delivered
        assert ev.deliv_fail == val.deliv_fail

        assert isinstance(e.id, int)
        assert isinstance(e.user_id, int)
        assert isinstance(e.state, str)
        assert isinstance(e.delivered, bool)
        assert isinstance(e.deliv_fail, bool)

    def test_update(self):
        with next(get_db()) as session:
            ev_1 = event.get_by_user_id(db = session, user_id=USER_ID)
            assert ev_1.delivered == False

            ev_1a = event.update(
                db = session, 
                db_obj=ev_1, 
                obj_in={"delivered": True})
            assert ev_1a.delivered == True
            assert ev_1a.user_id == USER_ID

    def test_delete(self):
        ev_1 = event.get_by_user_id(db = next(get_db()), user_id=USER_ID) 
        assert ev_1 is not None

        ev_1 = event.remove(db = next(get_db()), id=ev_1.id)
        assert ev_1 is not None

        ev_1 = event.get_by_user_id(db = next(get_db()), user_id=USER_ID) 
        assert ev_1 is None
