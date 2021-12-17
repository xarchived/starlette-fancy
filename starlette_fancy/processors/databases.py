from typing import List, Mapping

from databases import Database
from starlette.exceptions import HTTPException

from starlette_fancy.processors import Processor
from starlette_fancy.utils import where_clause_from_query_params


class DatabaseProcessor(Processor):
    database: Database
    insert_query: str
    select_query: str
    update_query: str
    delete_query: str

    async def post(self, validated_data: dict) -> dict:
        return dict(
            await self.database.fetch_one(
                query=self.insert_query,
                values=validated_data,
            )
        )

    async def get(self, validated_data: dict) -> List[dict]:
        conditions, values = where_clause_from_query_params(validated_data)
        return list(
            map(
                dict,
                await self.database.fetch_all(  # noqa
                    query=self.select_query + conditions,
                    values=values,
                ),
            )
        )

    async def patch(self, validated_data: dict) -> dict:
        record: Mapping = await self.database.fetch_one(
            query=self.update_query,
            values=validated_data,
        )
        if not record:
            raise HTTPException(status_code=404)
        return dict(record)

    async def delete(self, validated_data: dict) -> None:
        record: Mapping = await self.database.fetch_one(
            query=self.delete_query,
            values=validated_data,
        )
        if not record:
            raise HTTPException(status_code=404)
