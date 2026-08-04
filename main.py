from fastapi import FastAPI

from api.clients.app import router as client_router


app = FastAPI(
    title="Campaign CMS Clone"
)

app.include_router(
    client_router,
    tags=["Clients"]
)