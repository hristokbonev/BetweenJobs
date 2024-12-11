from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from companies.company_router import companies_router
from jobposts.jobpost_router import job_post_router
from dotenv import load_dotenv
from data.database import create_db, engine
# import uvicorn
from users.user_router import router as user_router
from resumes.resume_routers import router as resumes_router
from users.user_router import router as users_router
from utils.authentication import router as auth_router
from matches.match_router import match_router
# Add WEB Routers
from web_routers.home_router import router as index_router
from web_routers.jobposts_router import jobs_router
from web_routers.match_router import match_router
from web_routers.user_router import router as user_web_router
from web_routers.resumes_router import router as resumes_web_router
from web_routers.recruiter_router import router as recruiter_router
from web_routers.applications_router import router as applications_router
from web_routers.companies_router import company_router


load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db()
    try:
        yield 
    finally:
        engine.dispose()
        print("Database engine disposed and application shutting down...")

app = FastAPI(lifespan=lifespan)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(user_router)
app.include_router(resumes_router)
app.include_router(users_router)
app.include_router(companies_router)
app.include_router(job_post_router)
app.include_router(auth_router)
app.include_router(match_router)

app.include_router(index_router)
app.include_router(jobs_router)
app.include_router(user_web_router)
app.include_router(match_router)
app.include_router(resumes_web_router)
app.include_router(recruiter_router)
app.include_router(applications_router)
app.include_router(company_router)



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000)


