from datetime import datetime
from typing import Annotated

from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, mapped_column


class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy ORM models.
    Provides common functionality like table name generation.
    """

    type_annotation_map = {datetime: DateTime(timezone=True)}


T_CreatedAt = Annotated[
    datetime,
    mapped_column(server_default=func.current_timestamp(), nullable=False),
]

T_ModifiedAt = Annotated[
    datetime,
    mapped_column(server_default=func.current_timestamp(), server_onupdate=func.current_timestamp(), nullable=False),
]
