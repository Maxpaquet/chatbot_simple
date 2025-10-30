from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

# Configuration
SECRET_KEY = "secret"  # In production, use environment variables
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing context
PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")
MAX_LEN_CRYPT = 72  # Max length for bcrypt

# OAuth2 scheme
OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="token")

