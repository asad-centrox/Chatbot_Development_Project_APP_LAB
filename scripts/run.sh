
export $(cat .env | xargs)
echo "Running server on port $PORT"

MYPYPATH=./src mypy src/app/main.py


cd src/

uvicorn app.main:app --host 0.0.0.0 --port $PORT

cd ..
