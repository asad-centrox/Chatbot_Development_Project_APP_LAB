
export $(grep -v '^#' .env | xargs)
echo "Running server on port $PORT"

MYPYPATH=./src mypy src/app/main.py

if [ $? -ne 0 ]; then
    echo "Mypy had some errors. Please fix them before proceeding..."
    exit $?
fi

black src/
pylint -j4 src/
cd src/
uvicorn app.main:app --host 0.0.0.0 --port $PORT --reload
cd ..