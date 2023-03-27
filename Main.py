from fastapi import FastAPI
from routes.UserRoute import router as UserRoute
from routes.AuthRoute import router as AuthRoute
from routes.PostRoute import router as PostRoute
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.include_router(UserRoute, tags=["User"], prefix="/api/usuario")
app.include_router(AuthRoute, tags=["Auth"], prefix="/api/auth")
app.include_router(PostRoute, tags=["Post"], prefix='/api/postagem')

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins =["*"],
    allow_methods =['*'],
    allow_headers =['*'],
)


@app.get("/api/health", tags=["Health"])
async def health():
    return {
        'message': 'ok'
    }
