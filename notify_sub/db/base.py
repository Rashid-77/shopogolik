# Import all the models, so that Base has them before being
# imported by Alembic
from models.user_lim import User  # noqa

from .base_class import Base  # noqa
