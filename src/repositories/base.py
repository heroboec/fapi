from pydantic import BaseModel
from sqlalchemy import select, insert, delete, func, update

from src.schemas.hotels import Hotel


class BaseRepository:
    model = None
    schema: BaseModel = Hotel

    def __init__(self, session):
        self.session = session

    def __del__(self):
        # self.session.close()
        pass

    async def get_filtered(self, **filters):
        query = select(self.model).filter_by(**filters)
        result = await self.session.execute(query)
        return [self.schema.model_validate(item, from_attributes=True) for item in result.scalars()]

    async def get_all(self, *args, **kwargs):
        return await self.get_filtered()

    async def get_one_or_none(self, **filters):
        query = select(self.model).filter_by(**filters)
        result = await self.session.execute(query)
        res = result.scalars().one_or_none()
        if not res:
            return res

        return self.schema.model_validate(res, from_attributes=True)

    async def add(self, data: BaseModel):
        add_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(add_stmt)

        res = result.scalars().one()
        return self.schema.model_validate(res, from_attributes=True)

    async def edit(self, data: BaseModel, **filters):
        """
        Заменяет все поля в базе по фильтрам.
        :param data: данные для замены
        :param filters: фильтры
        :return: None
        """
        edit_stmt = update(self.model).filter_by(**filters).values(**data.model_dump())
        await self.session.execute(edit_stmt)

    async def update(self, data: BaseModel, exclude_unset: bool, **filters):
        """
        Заменяет некоторые поля в базе по фильтрам.
        :param data: данные для замены
        :param filters: фильтры
        :return: None
        """
        upd_stmt = update(self.model).filter_by(**filters).values(**data.model_dump(exclude_unset=exclude_unset))
        await self.session.execute(upd_stmt)

    async def delete(self, **filters):
        del_stmt = delete(self.model).filter_by(**filters)
        await self.session.execute(del_stmt)
