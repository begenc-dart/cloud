from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from core.database import Base,engine
import routers
from routers.auth import auth_router

app = FastAPI()


origins = ["*"]
methods = ["*"]
headers = ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=methods,
    allow_headers=headers,
)
app.mount('/uploads', StaticFiles(directory="uploads"), name="uploads")
Base.metadata.create_all(engine)
app.include_router(auth_router)
app.include_router(routers.banner_router)
app.include_router(routers.shared_router )
app.include_router(routers.folder_api)
