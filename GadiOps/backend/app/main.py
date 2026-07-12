from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.core.database import engine, Base
# Add this import near the top of backend/app/main.py
from app.routers import auth
# Import the vehicle routing module
from app.routers import vehicles
# Import the driver routing module
from app.routers import drivers

from app.routers import trips

from app.routers import expenses

from app.routers import dashboard

from fastapi import FastAPI
from app.core.database import engine, Base
import app.models  # Registers your newly cleaned models directory layout

app = FastAPI(title="GadiOps API")

# Safely reset any cached model states during hot-reloads
Base.metadata.clear()

# Rebuild all database tables cleanly
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="GadiOps API",
    description="Smart Transport Operations Platform API",
    version="1.0.0"
)

# Configure CORS (Allows smooth API interaction)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Health Check Route
@app.get("/api/health", tags=["System"])
def health_check():
    return {"status": "healthy", "platform": "GadiOps"}

# =====================================================================
# ROUTERS IMPORT & REGISTRATION (Uncomment as you build them)
# =====================================================================
# from app.routers import auth, dashboard, vehicles, drivers, trips, expenses
# app.include_router(auth.router, prefix="/api")
# app.include_router(dashboard.router, prefix="/api")
# app.include_router(vehicles.router, prefix="/api")
# app.include_router(drivers.router, prefix="/api")
# app.include_router(trips.router, prefix="/api")
# app.include_router(expenses.router, prefix="/api")


# Mount Frontend Assets (Serves index.html at root '/' and everything in frontend/)
# Register the router inside backend/app/main.py (uncomment or add line)
app.include_router(auth.router, prefix="/api")
# Always place this at the bottom so it doesn't hijack API route matching
app.mount("/", StaticFiles(directory="../frontend", html=True), name="frontend")
# Mount inside the FastAPI instance structure
app.include_router(vehicles.router, prefix="/api")

# Mount inside the FastAPI instance structure
app.include_router(drivers.router, prefix="/api")

app.include_router(trips.router, prefix="/api")

app.include_router(expenses.router, prefix="/api")

app.include_router(dashboard.router, prefix="/api")