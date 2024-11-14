from fastapi import APIRouter, HTTPException

from users.user_models import UserRegistrationRequest
from users import user_service as us

users_router = APIRouter(prefix='/api/users', tags=["Users"])

@users_router.get('/')
def show_users():
    try:
        return us.view_users()
    except ValueError as e:
        return HTTPException(status_code=404, detail=str(e))


# @users_router.post('/register')
# def register_user(new_usr: UserRegistrationRequest):
#     try:
#         us.create_user(
#             new_usr.username,
#             new_usr.password,
#             new_usr.first_name,
#             new_usr.last_name,
#             new_usr.date_of_birth,
#             new_usr.email
#         )
#     except ValueError as e:
#         return HTTPException(status_code=404, detail=str(e))