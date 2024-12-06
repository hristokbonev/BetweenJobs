from fastapi import APIRouter, Request, Depends
from starlette.templating import Jinja2Templates
from data.database import get_session
from sqlmodel import Session
from utils import attribute_service as ats
from utils import auth as au


index_router = APIRouter(prefix='')
templates = Jinja2Templates(directory='templates')


@index_router.get('/')
def index(request: Request):
    return templates.TemplateResponse(request=request, name='index.html')
    

@index_router.get('/home')
def index(request: Request, session: Session = Depends(get_session)):
    locations = list(ats.get_all_locations(session))
    token = request.cookies.get('token')
    if token:
        user = au.get_current_user(token)
        print(user)
        return templates.TemplateResponse(
            request=request, 
            name='home.html',                        
            context={
                'request': request, 
                'user': user,
                'locations': locations
            })

    else:
        return templates.TemplateResponse(request=request, name='home.html')
    
    