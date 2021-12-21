# Starlette Fancy

We add two more layer on top of Starlette: "validator" and "processor".
Validators are responsible for data validations and processors do logic of the
web app.

## Installation

To install base package:

```bash
pip install starlette-fancy
```

we use "pydantic" package for "PydanticValidator" and "databases" package for
"DatabaseProcessor" and to support different JSON libraries we use
"starlette-marshal" package. You can install each with following commands:

```bash
pip install starlette-fancy[pydantic]
pip install starlette-fancy[databases]
pip install starlette-fancy[starlette-marshal]
```

to install all packages at once:

```bash
pip install starlette-marshal[full]
```

## Validators

In validator layer we receive data from a request then validate them and return
validated data. Input data can come from request body, querystring and sometimes
in could be response body.

We don't specify any library or method to validate data. One may create its own
validator from the scratch. All you need to do is to inherit from "Validator"
class and then implement its ```__call__``` method.

an example could be like this:

```python
class CustomValidator(Validator):
    async def __call__(
            self,
            data: Union[list, dict],
            source: Literal["body", "query_params"] = "body",
            response: bool = False,
            partial: bool = False,
    ) -> dict:
        ...
```

### PydanticValidator

There is built in validator that powered with Pydantic library. First you have
to create models:

```python
class PostParams(BaseModel):
    title: str
    slug: str
    content: str
    published_at: datetime


class PostBody(BaseModel):
    id: Optional[UUID]
```

now we can have a simple validator like this:

```python
class PostValidator(PydanticValidator):
    params_model = PostParams
    request_model = PostBody
```

## Processors

Processor layer is after validator, and it receives validated data. In this
layer we write logic of our program, and we return the processed. You should
inherit from "Processor" class and then override one of "get", "post", "put",
"delete" or "patch" methods. Here an example:

```python
class CustomProcessor(Processor):
    async def get(self, validated_data: dict) -> Any:
        return {
            'validated_data': validated_data,
        }
```

### DatabaseProcessor

A common scenario is when we want to map an HTTP method to a database query.
Suppose we have the following queries:

```python
INSERT_POSTS: str = '''
    insert into posts (title, slug, content, published_at)
    values (:title, :slug, :content, :published_at)
    returning *
'''

SELECT_POSTS: str = '''
    select id, title, slug, content, published_at
    from posts
    where true
'''

UPDATE_POSTS: str = '''
    update posts
    set title        = coalesce(:title, title),
        slug         = coalesce(:slug, slug),
        content      = coalesce(:content, content),
        published_at = coalesce(:published_at, published_at)
    where id = :id
    returning *
'''

DELETE_POSTS: str = '''
    delete
    from posts
    where id = :id
    returning *
'''
```

now a DatabaseProcessor example is like this:

```python
database: Database = Database(url=DATABASE_URL)


class PostProcessor(DatabaseProcessor):
    database = database
    insert_query = INSERT_POSTS
    select_query = SELECT_POSTS
    update_query = UPDATE_POSTS
    delete_query = DELETE_POSTS
```

## Endpoints

This isn't a new thing, just normal Starlette endpoint. But we only handle
request and response in this layer. We get request and pass the values to
validator then receive validated data and give it to processor layer. At the end
we create a response with what processor returned to us.

Here an example:

```python
class CustomEndpoint(Endpoint):
    validator: Validator
    processor: Processor

    async def get(self, request: Request) -> Response:
        query_params: dict = dict(request.query_params)

        validated_data: dict = await self.validator(
            data=query_params,
            source="query_params",
        )
        processed_data: list = await self.processor.get(
            validated_data=validated_data,
        )

        return JSONResponse(content=processed_data)
```

### CRUDEndpoint
To create a fast CRUD endpoint you can use this class. With "PydanticValidator"
and "DatabaseProcessor" it's really simple:

```python
class PostEndpoint(CRUDEndpoint):
    validator = PostValidator()
    processor = PostProcessor()
```

there's a function to generate routes for our CRUD resource:

```python
routes = generate_crud_routes('/posts', endpoint=PostEndpoint, id_type='uuid')
```

## TODO

- [x] Pydantic validator
- [ ] marshmallow validator
- [ ] ORM processor
- [x] database processor
- [x] CRUD endpoint
- [ ] gRPC endpoint
- [ ] proxy endpoint
