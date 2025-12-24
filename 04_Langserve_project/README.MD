## Backend Setup

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

## backend Run

cd backend
uvicorn app.main:app --reload

## cors 
1. backend is running localhost:8000
```Python
cd backend 
uvicorn app.main:app --reload
```
2. frontend is running localhost:3000
```Python
cd .\frontend-web\
npm run dev
```
3. so api will face the cors issue and can be fixed by adding middleware
```Python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```
## backend NOTE
### 1. need to lock app version and add requirements-dev.txt for dev
$ > pip freeze > requirements.lock.txt

### 2. do not name file as app.py and fastapi, or some misleading keyword
### 3. set backend dir as Source Root
### 4. always add directory as new -> Python package.


## Frontend setup
npx create-next-app@latest frontend-web
