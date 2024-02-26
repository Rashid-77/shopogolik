from datetime import datetime
from typing import Any, Dict, Optional, Union

from crud.base import CRUDBase
from models.product import Product
from schemas.product import ProductCreate, ProductUpdate
from sqlalchemy.orm import Session


class CRUDProduct(CRUDBase[Product, ProductCreate, ProductUpdate]):
    def get(self, db: Session, id: int) -> Optional[Product]:
        return db.query(self.model).filter(self.model.id == id).first()

    def create(self, db: Session, *, obj_in: ProductCreate) -> Product:
        db_obj = Product(
            sku=obj_in.sku,
            name=obj_in.name,
            price=obj_in.price,
            weight_kg=obj_in.weight_kg,
            width_m=obj_in.width_m,
            length_m=obj_in.length_m,
            height_m=obj_in.height_m,
            volume_m3=obj_in.volume_m3,
            carDescr=obj_in.carDescr,
            shortDescr=obj_in.shortDescr,
            longDescr=obj_in.longDescr,
            thumb=obj_in.thumb,
            image=obj_in.image,
            updDate=datetime.now(),
            live=obj_in.live,
            virtual=obj_in.virtual,
            unlimited=obj_in.unlimited,
            location=obj_in.location,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: Product,
        obj_in: Union[ProductUpdate, Dict[str, Any]],
    ) -> Product:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def is_product_exists(self, db: Session, *, name: str) -> Optional[Product]:
        return db.query(Product).filter(Product.name == name).first()


product = CRUDProduct(Product)
