from typing import Callable, List, Tuple, Literal

from starlette.routing import Route

OP_MAP = {
    "like": "like",
    "lt": "<",
    "lte": "<=",
}


def where_clause_from_query_params(query_params: dict) -> Tuple[str, dict]:
    query: str = ""
    values: dict = {}
    for k, v in query_params.items():
        if v is None:
            continue

        parts: list = k.split("__")
        len_parts: int = len(parts)

        if len_parts == 1:
            field = parts[0]
            op = "="
        elif len_parts == 2:
            field = parts[0]
            op = OP_MAP[parts[1]]
        else:
            raise ValueError('There should be only one "__" in field name')

        query += f" and {field} {op} :{field}"
        values[field] = v

    return query, values


def generate_crud_routes(
    path: str,
    endpoint: Callable,
    id_type: Literal["int", "uuid", "str"] = "int",
) -> List[Route]:
    assert not path.endswith("/"), "path must not end with '/'"

    return [
        Route(
            path=f"{path}/{{id:{id_type}}}",
            endpoint=endpoint,
            methods=["delete", "patch"],
        ),
        Route(
            path=path,
            endpoint=endpoint,
            methods=["get", "post"],
        ),
    ]
