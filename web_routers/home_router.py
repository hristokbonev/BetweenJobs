from fastapi import APIRouter, Request, Depends, Form
from data.database import get_session
from sqlmodel import Session
from utils import attribute_service as ats
from utils import auth as au
from common.template_config import CustomJinja2Templates

router = APIRouter(prefix='')
templates = CustomJinja2Templates(directory='templates')


@router.get('/')
def index(request: Request):
    return templates.TemplateResponse(request=request, name='index.html')
    

@router.get('/home')
def serve_home(request: Request, session: Session = Depends(get_session)):
    locations = list(ats.get_all_locations(session))
    employments = list(ats.get_all_employments(session))

    token = request.cookies.get('token')
    context={
        'request': request, 
        'locations': locations,
        'employments': employments,
        'filters': {
            'search_field': None,
            'keyword': None
        }
    }

    if token:
        user = au.get_current_user(token)
        context['user'] = user

    return templates.TemplateResponse(
        request=request,
        name='home.html', 
        context=context
    )
        

# # Utility function for rendering search resuls in search()
# def _get_search_data(
#     btnjobs: str = Form(...),
#     btncompanies: str = Form(...),
#     btnresumes: str = Form(...),
#     region: str = Form(...),
#     job_type: str = Form(...)
# ):
#     return btnjobs, btncompanies, btnresumes, region, job_type


# @index_router.post('/home')
# def search_category(
#     request: Request, 
#     session: Session = Depends(get_session),
#     form_data = Depends(_get_search_data)
# ):
#     # Unpack selected url navigation
