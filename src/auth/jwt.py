from fastapi import Request,Depends,HTTPException, status
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from src.database.session import get_db
from src.models.user import User
from src.core.security import SECRET_KEY, ALGORITHM

def get_current_user(
        request: Request,
        db: Session = Depends(get_db)
):

    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        email: str | None = payload.get("sub")

        if email is None:
            raise HTTPException(status_code=401)

    except JWTError:
        raise HTTPException(status_code=401)

    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=401)

    return user

def required_admin(current_user = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso restrito a administradores"
        )
    return current_user