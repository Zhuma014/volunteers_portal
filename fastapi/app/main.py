from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app import models
from app.routers.auth import router as auth_router
from app.routers.profile import router as profile_router
from app.routers.cases import router as cases_router
from app.routers import staff_cases
from app.routers import statements
from app.routers import meta



Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Antikor Case Management API",
    description="API для подачи и обработки жалоб и заявлений",
    version="1.0.0"
)

# ✅ Add CORS middleware here
origins = [
    "http://localhost:5173",  # Vue dev server
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # or ["*"] for all origins (not recommended for production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Include routers
app.include_router(auth_router, prefix="/auth")
app.include_router(profile_router)
app.include_router(cases_router)
app.include_router(staff_cases.router)
app.include_router(statements.router)
app.include_router(meta.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
