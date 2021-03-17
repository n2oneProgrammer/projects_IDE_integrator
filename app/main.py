from fastapi import FastAPI
from starlette.responses import RedirectResponse

from .database import Base, engine
from .routers import project,project_type

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Fundacyjni API", description="", version="0.0.1")
app.include_router(project.router)
app.include_router(project_type.router)


@app.get("/")
async def root():
    response = RedirectResponse(url="/docs")
    return response
