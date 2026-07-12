import os
from datetime import datetime, timedelta, timezone
from typing import Optional
import bcrypt
from jose import jwt, JWTError

# Security Configuration Defaults (Override via backend/.env)
SECRET_KEY = os.getenv("JWT_SECRET", "super-secret-gadiops-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 480  # 8 hours matching the hackathon duration

# ==========================================
# PASSWORDS UTILITIES (Native Bcrypt)
# ==========================================
def hash_password(password: str) -> str:
    """Hashes a plain text password safely using a random salt."""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Compares a plain text password with a stored hash."""
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), 
        hashed_password.encode("utf-8")
    )

# ==========================================
# JWT TOKEN HANDLING
# ==========================================
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Generates a secure JSON Web Token payload containing authorization claims."""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt