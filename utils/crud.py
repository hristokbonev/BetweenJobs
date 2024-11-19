from data.db_models import User
from users.user_models import UserCreate
from sqlmodel import select, Session
from users.user_models import UserModel

def create_user(db: Session, user: UserCreate):

    date_of_birth = user.date_of_birth if user.date_of_birth else None

    db_user = User(username=user.username,
                    password=user.password,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    is_admin=user.is_admin,
                    date_of_birth=date_of_birth,
                    email=user.email
                )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(username: str, session: Session) -> UserCreate:
        statement = select(User).where(User.username == username)
        user = session.exec(statement).first()
        if not user:
            return None
        return UserModel(**user.model_dump())


def get_user_by_username(session: Session, username: str):
    statement = select(User).where(User.username == username)
    return session.exec(statement).first()

  
    
    


