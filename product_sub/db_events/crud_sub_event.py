# from typing import Any, Optional, Dict, Union
# from sqlalchemy.orm import Session

# from crud.base import CRUDBase
# from models.sub_event import SubEvent
# from order.schemas.sub_event import SubEventCreate, SubEventUpdate


# class SubEventUtils():

#     def get(self, db: Session, id: int) -> Optional[SubEvent]:
#         return db.query(self.model).filter(self.model.uuid == id).first()

#     def create(self, db: Session, *, obj_in: SubEventCreate, user_id) -> SubEvent:
#         db_obj = SubEvent(
#             uuid = obj_in.uuid,
#             userId = user_id,
#             goods_reserved = obj_in.goods_reserved,
#             money_reserved = obj_in.money_reserved,
#             courier_reserved = obj_in.courier_reserved,
#         )
#         db.add(db_obj)
#         db.commit()
#         db.refresh(db_obj)
#         return db_obj

#     def update(
#         self, db: Session, *, db_obj: SubEvent, obj_in: Union[SubEventUpdate, Dict[str, Any]]
#     ) -> SubEvent:
#         if isinstance(obj_in, dict):
#             update_data = obj_in
#         else:
#             update_data = obj_in.model_dump(exclude_unset=True)
#         return super().update(db, db_obj=db_obj, obj_in=update_data)

#     def is_order_exists(self, db: Session, *, id: int) -> Optional[SubEvent]:
#         return db.query(SubEvent).filter(SubEvent.id == id).first()


# sub_event = CRUDSubEvent(SubEvent)
