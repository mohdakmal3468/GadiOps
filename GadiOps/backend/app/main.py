import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.database import engine, Base
import app.models  # Registers your database models layout

# Import routing modules
from app.routers import auth, vehicles, drivers, trips, expenses, dashboard

# 1. Trigger database table creation cleanly
Base.metadata.create_all(bind=engine)

# 2. Initialize a single FastAPI instance
app = FastAPI(
    title="GadiOps API",
    description="Smart Transport Operations Platform API",
    version="1.0.0"
)

# 3. Configure CORS (Allows smooth API interaction)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4. Global Health Check Route
@app.get("/api/health", tags=["System"])
def health_check():
    return {"status": "healthy", "platform": "GadiOps"}

# 5. Register ALL API Routers (Must be registered BEFORE mounting frontend)
app.include_router(auth.router, prefix="/api")
app.include_router(vehicles.router, prefix="/api")
app.include_router(drivers.router, prefix="/api")
app.include_router(trips.router, prefix="/api")
app.include_router(expenses.router, prefix="/api")
app.include_router(dashboard.router, prefix="/api")

# 6. Mount Frontend Assets (ALWAYS place this at the very bottom)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # points to backend/
FRONTEND_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "frontend"))

if os.path.exists(FRONTEND_DIR):
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
else:
    print(f"Warning: Frontend directory not found at {FRONTEND_DIR}. Skipping static mount.")