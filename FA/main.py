from fastapi import FastAPI, Depends, HTTPException, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.requests import Request
from sqlalchemy import create_engine, Column, String, MetaData, select
from sqlalchemy.ext.declarative import declarative_base
from databases import Database
from starlette.middleware.sessions import SessionMiddleware
from fastapi.staticfiles import StaticFiles

DATABASE_URL = "mysql+pymysql://root:0000@127.0.0.1:3306/security"

database = Database(DATABASE_URL)
metadata = MetaData()

app = FastAPI()

# 'static' 디렉토리에 있는 정적 파일을 '/static' 경로로 제공합니다.
app.mount("/static", StaticFiles(directory="static"), name="static")

# 세션 미들웨어 추가
app.add_middleware(SessionMiddleware, secret_key="your-secret-key")

templates = Jinja2Templates(directory="templates")

Base = declarative_base()

class User(Base):
    __tablename__ = "security"
    sec_id = Column(String, primary_key=True, index=True)
    sec_pw = Column(String)
    sec_nm = Column(String)
    sec_bir = Column(String)
    sec_add = Column(String)
    sec_hp = Column(String)
    sec_area = Column(String)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    user_id = request.session.get("user_id")
    user = None
    if user_id:
        query = select(User).where(User.sec_id == user_id)
        user = await database.fetch_one(query)
    return templates.TemplateResponse("index.html", {"request": request, "user": user})

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login/")
async def login(request: Request, sec_id: str = Form(...), sec_pw: str = Form(...)):
    query = select(User).where(User.sec_id == sec_id)
    user = await database.fetch_one(query)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.sec_pw != sec_pw:
        raise HTTPException(status_code=400, detail="Incorrect password")
    
    request.session["user_id"] = sec_id
    return RedirectResponse(url="/", status_code=303)

@app.get("/logout/")
def logout(request: Request):
    if "user_id" in request.session:
        del request.session["user_id"]
    return RedirectResponse(url="/", status_code=303)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
