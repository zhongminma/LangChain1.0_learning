Follow the LangChain v1.0 office docs as reference

##  build-up env 
#### a. installation
#### b. pip package
#### c. Gemini and OpenAI llm setup

## 1. 01_basic_examples
#### a. llm + prompt + chain
#### b. string, pydantic and structured output sample
#### c. XML output (AoP-like enhancement)

## 2. 02_prompt_template_examples
#### a. string prompt template 
#### b. chat_prompt_template
#### c. fewshot prompt template
#### c. fewshot selector (example selector)

## 3. 03_runnable_examples
#### a. stream 
#### b. astream
#### c. stream events
#### d. token usage (BaseCallBackHandler)

## 4. 04_langserve_project
#### a. llm backend and next.js frontend (check read.md for setup)
#### b. chat history with session_id + InMemory and session_id + redis
#### c. chat history with user_id + conversation_id
#### d. Add redis RunnableWithMessageHistory 
#### f. config LangSmith usage : https://smith.langchain.com/

## 5. 05_tool_examples
#### a. tool decorator
#### b. StructuredTool with async and coroutine args is required

## 6. 06_agent_examples
#### a. agent invoke
#### b. agent invoke how to debug
#### c. agent streaming with a tool
#### d. agent streaming with multiple tools

## 7. 07__middleware_and_utils
#### a. Memory (InMemoryChatMessageHistory)
#### b. redis or DB
#### c. token usage
#### d. rate limiter
#### e. logger

## 6. 06_handlers
#### a. error handler