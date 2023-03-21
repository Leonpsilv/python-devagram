from fastapi import FastAPI
from routes.UserRoute import router as UserRoute
from routes.AuthRoute import router as AuthRoute

app = FastAPI()
app.include_router(UserRoute, tags=["User"], prefix="/api/usuario")
app.include_router(AuthRoute, tags=["Auth"], prefix="/api/auth")


@app.get("/api/health", tags=["Health"])
async def health():
    return {
        'message': 'ok'
    }
