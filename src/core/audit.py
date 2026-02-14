from sqlalchemy.orm import Session
from src.models.audit import Audit


def log_action(
    db: Session,
    user_id: int,
    action: str
):

    log = Audit(
        user_id=user_id,
        action=action
    )

    db.add(log)
    db.commit()
