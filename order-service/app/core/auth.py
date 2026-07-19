from app.core.config import settings
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM

security = HTTPBearer();

def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(security))-> int:
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if(user_id is None):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
        return int(user_id)
    except JWTError as e:
        print(f'fucking error we will push through this :  {e}')
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid or expired token",  headers={"WWW-Authenticate": "Bearer"},)
    



  