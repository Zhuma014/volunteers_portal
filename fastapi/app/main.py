from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app import models  # noqa: F401
from app.routers.auth import router as auth_router
from app.routers.profile import router as profile_router
from app.routers.cases import router as cases_router
from app.routers import staff_cases
from app.routers import statements
from app.routers import meta
from app.routers import canvas_enrollments



Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Antikor Case Management API",
    description="API для подачи и обработки жалоб и заявлений",
    version="1.0.0"
)

# ✅ Add CORS middleware here
origins = [
    "http://localhost:5173",  # Vue dev server
    "http://127.0.0.1:5173",  # Also allow 127.0.0.1 if used
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # or ["*"] for all origins (not recommended for production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Include routers
app.include_router(auth_router, prefix="/api/auth")
app.include_router(profile_router, prefix="/api")
app.include_router(cases_router, prefix="/api")
app.include_router(staff_cases.router, prefix="/api")
app.include_router(statements.router, prefix="/api")
app.include_router(meta.router,prefix="/api")
app.include_router(canvas_enrollments.router, prefix="/api")



@app.get("/")
async def root():
    return {"message": "Hello World"}
