from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer


app = FastAPI(
    docs_url='/docs',
    title='Secret Manager API',
    debug=True
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token', auto_error=False)
