from fastapi import Depends, HTTPException, status
from src.core.deps import get_current_user
from src.models.user import User


def require_admin(
    current_user: User = Depends(get_current_user),
) -> User:

    print("USER:", current_user.email)
    print("ROLE:", current_user.role.name if current_user.role else "SEM ROLE")
    print("ACTIVE:", current_user.is_active)

    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário inativo"
        )

    if not current_user.role:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário sem função atribuída"
        )

    if current_user.role.name.strip().lower() != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso restrito a administradores"
        )

    return current_user
