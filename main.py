import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from database.connection import Settings
from routes.users import user_router
from routes.events import event_router


settings = Settings
origins = ["*"]


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    await settings().initialize_database()
    yield  # This pauses the lifespan function until shutdown
    # Shutdown logic
    print("Shutting down the application...")


app = FastAPI(lifespan=lifespan)


app.include_router(user_router, prefix="/user")
app.include_router(event_router, prefix="/event")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
