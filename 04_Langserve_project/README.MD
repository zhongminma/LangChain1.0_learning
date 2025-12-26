## 1. setup 
### Backend Setup
```Python
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Frontend setup
```Python
npx create-next-app@latest frontend-web
```

## 2. backend & frontend Run
a. backend is running localhost:8000
```Python
cd backend
uvicorn app.main:app --reload
```
b. frontend is running localhost:3000
```Python
cd .\frontend-web\
npm run dev
```
c. cors config in backend
Api call will face cors issue so it need to handle in the middleware
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
d. backend NOTE
#### d1. need to lock app version and add requirements-dev.txt for dev
$ > pip freeze > requirements.lock.txt
#### d2. set backend dir as Source Root and always add directory as new -> Python package.

## 3. add chat history
### 3.1  session_id + memory
backend workflow
```markdown
session_id 
-> in memory dict [session_id] 
-> InMemoryChatMessageHistory stores history 
-> RunnableWithMessageHistory make runnable 
-> LLM inject history
```

### 3.2 user_id + conversation_id