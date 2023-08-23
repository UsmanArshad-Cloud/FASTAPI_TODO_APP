from fastapi import FastAPI, Depends
from routers import auth, todos,users
from company import companyapis, dependencies
from Database import engine
import Models

app = FastAPI()

Models.Base.metadata.create_all(bind=engine)  # Creating Tables

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(companyapis.router,
                   prefix="/companyapis",
                   tags=["Company API"],
                   dependencies=[Depends(dependencies.get_token_header)],
                   responses={418: {"description": "Internal User Only"}})
app.include_router(users.router)
