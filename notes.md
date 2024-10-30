To start server with auto reload: `uvicorn src.main:app --reload`

Schema models: Pydantic
    - define the structure of the http requests and response
    - handles some data validation for post requests

SQLAlchemy models:
    - defines the columns of the tables
    - handles CRUD queries to the DB

Alembic: 
- `alembic revision -m "<message>"`
- `alembic upgrade head | <revision number>`
- `alembic downgrade -1 | -x`
- `alembic history`
