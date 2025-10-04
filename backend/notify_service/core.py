from fastapi import FastAPI


app = FastAPI(
    docs_url='/docs',
    title='Notification Service API',
    debug=True
)
