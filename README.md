# START

uvicorn main:app --reload

# MIGRATIONS

alembic revision --autogenerate -m "create_xxx_table"
alembic upgrade head
