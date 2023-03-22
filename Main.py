from fastapi import FastAPI
from routes.UserRoute import router as UserRoute
from routes.AuthRoute import router as AuthRoute
from routes.PostRoute import router as PostRoute

app = FastAPI()
app.include_router(UserRoute, tags=["User"], prefix="/api/usuario")
app.include_router(AuthRoute, tags=["Auth"], prefix="/api/auth")
app.include_router(PostRoute, tags=["Post"], prefix='/api/postagem')


@app.get("/api/health", tags=["Health"])
async def health():
    return {
        'message': 'ok'
    }
