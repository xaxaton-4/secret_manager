from fastapi import FastAPI

from ws.views import router as ws_router


app = FastAPI(
    docs_url='/docs',
    title='Notification Service API',
    debug=True
)
app.include_router(ws_router)
