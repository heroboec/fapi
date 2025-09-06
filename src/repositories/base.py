from pydantic import BaseModel
from sqlalchemy import select, insert, delete, func, update


class BaseRepository:
    model = None

    def __init__(self, session):
        self.session = session

    def __del__(self):
        # self.session.close()
        pass

    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_one_or_none(self, **filters):
        query = select(self.model).one_or_none(**filters)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()

    async def add(self, data: BaseModel):
        add_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(add_stmt)

        return result.scalars().one()

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
