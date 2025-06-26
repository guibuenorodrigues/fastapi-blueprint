# app/crud/base.py

from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase  # Your base ORM model class

ModelType = TypeVar("ModelType", bound=DeclarativeBase)
CreateSchemaType = TypeVar("CreateSchemaType", bound=Any)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=Any)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Base class for common CRUD operations.
    T is the SQLAlchemy model, CreateSchemaType and UpdateSchemaType are Pydantic schemas.
    """

    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(self, db: AsyncSession, obj_id: Any) -> Optional[ModelType]:
        """Retrieve a single object by its ID."""
        result = await db.execute(sa.select(self.model).where(self.model.id == obj_id))
        return result.scalar_one_or_none()

    async def get_multi(
        self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        """Retrieve multiple objects with pagination."""
        result = await db.execute(sa.select(self.model).offset(skip).limit(limit))
        return list(result.scalars().all())

    async def create(self, db: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        """Create a new object."""
        db_obj = self.model(**obj_in.model_dump())  # Use model_dump for Pydantic v2
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
        self,
        db: AsyncSession,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        """Update an existing object."""
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(
                exclude_unset=True
            )  # Exclude unset fields for partial update

        for field, value in update_data.items():
            setattr(db_obj, field, value)

        db.add(db_obj)  # Add to session to mark as dirty
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def remove(self, db: AsyncSession, *, obj_id: int) -> Optional[ModelType]:
        """Remove an object by its ID."""
        stmt = (
            sa.delete(self.model).where(self.model.id == obj_id).returning(self.model)
        )
        result = await db.execute(stmt)
        removed_obj = result.scalar_one_or_none()
        await db.commit()
        return removed_obj
