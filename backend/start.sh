#!/bin/bash
# run alembic and uvicorn then
cd alembic/
alembic upgrade head
cd ../app/
uvicorn main:app --host 0.0.0.0
