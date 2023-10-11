### 필요 라이브러리 등
from fastapi import FastAPI, Depends, HTTPException, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.requests import Request
from sqlalchemy import create_engine, Column, String, MetaData, select
from sqlalchemy.ext.declarative import declarative_base
from databases import Database
from starlette.middleware.sessions import SessionMiddleware
from fastapi.staticfiles import StaticFiles
from py_vapid import Vapid
from pywebpush import webpush, WebPushException
import requests


### 서버 실행 코드: uvicorn main:app --reload ###

# 데이터베이스 연결 URL 설정
DATABASE_URL = "mysql+pymysql://root:0000@127.0.0.1:3306/security"


# 데이터베이스 객체 생성
database = Database(DATABASE_URL)
metadata = MetaData()
# VAPID 설정
#VAPID_PRIVATE_KEY = "cbjV5JCGvpYPoAj0kpMqCIBR8f_k6Z74cTE"
#VAPID_PUBLIC_KEY = "BPwPP1HTMHD9YjUT9ZCYXyNuv3rt5Ytz8cftZQHWBOBolFBIWDRSbansTNeV2mBhgUsVQsYfZ0M-hitkcCZu2v0"
#VAPID_CLAIMS = {
#    "sub": "mailto:yulha042812@gmail.com"
#}

# FastAPI 앱 객체 생성
app = FastAPI()

# 'static' 디렉토리의 정적 파일을 '/static' 경로로 제공
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/bootstrap", StaticFiles(directory="bootstrap"), name="bootstrap")
app.mount("/css", StaticFiles(directory="css"), name="css")
app.mount("/js", StaticFiles(directory="js"), name="js")
app.mount("/templates", StaticFiles(directory="templates"), name="templates")

#########################################################
# 세션 미들웨어 추가 (사용자 세션 관리를 위함)
app.add_middleware(SessionMiddleware, secret_key="your-secret-key")

# Jinja2 템플릿 설정
templates = Jinja2Templates(directory="templates")

# SQLAlchemy의 기본 클래스 생성
Base = declarative_base()

# User 모델 정의
class User(Base):
    __tablename__ = "security"
    sec_id = Column(String, primary_key=True, index=True)
    sec_pw = Column(String)
    sec_nm = Column(String)
    sec_bir = Column(String)
    sec_add = Column(String)
    sec_hp = Column(String)
    sec_area = Column(String)



# 루트 경로에 대한 핸들러
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    user_id = request.session.get("user_id")
    user = None
    if user_id:
        query = select(User).where(User.sec_id == user_id)
        user = await database.fetch_one(query)
    return templates.TemplateResponse("index.html", {"request": request, "user": user})

@app.get("/favicon.ico")
async def favicon():
    return {}


# 모든 페이지에 대한 핸들러
@app.get("/{page}", response_class=HTMLResponse)
async def read_page(request: Request, page: str):
    user_id = request.session.get("user_id")
    user = None
    if user_id:
        query = select(User).where(User.sec_id == user_id)
        user = await database.fetch_one(query)
    
    return templates.TemplateResponse(f"{page}.html", {"request": request, "user": user})

# 로그인 페이지에 대한 핸들러
@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# 가입 페이지에 대한 핸들러
@app.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@app.post("/login/")
async def login(request: Request, sec_id: str = Form(...), sec_pw: str = Form(...)):
    query = select(User).where(User.sec_id == sec_id)
    user = await database.fetch_one(query)
    if not user:
        return templates.TemplateResponse("login.html", {"request": request, "error": "입력한 ID 정보가 없습니다."})
    if user.sec_pw != sec_pw:
        return templates.TemplateResponse("login.html", {"request": request, "error": "패스워드가 잘못되었습니다."})
    
    request.session["user_id"] = sec_id
    return RedirectResponse(url="/", status_code=303)



# 로그아웃 처리 핸들러
@app.get("/logout/")
def logout(request: Request):
    if "user_id" in request.session:
        del request.session["user_id"]
    return RedirectResponse(url="/", status_code=303)

# 앱 시작 시 데이터베이스 연결
@app.on_event("startup")
async def startup():
    await database.connect()

# 앱 종료 시 데이터베이스 연결 해제
@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

### 회원 가입 기능 추가
@app.post("/signup")
async def signup(
    request: Request,
    sec_id: str = Form(...),
    sec_pw: str = Form(...),
    sec_nm: str = Form(...),
    sec_bir: str = Form(...),
    sec_hp: str = Form(...),
    sec_add: str = Form(...),
    sec_area: str = Form(...)
):
    # 이미 존재하는 사용자인지 확인
    query = select(User).where(User.sec_id == sec_id)
    user = await database.fetch_one(query)
    if user:
        raise HTTPException(status_code=400, detail="User ID already exists")

    # 사용자 정보 저장
    query = User.__table__.insert().values(
        sec_id=sec_id,
        sec_pw=sec_pw,
        sec_nm=sec_nm,
        sec_bir=sec_bir,
        sec_hp=sec_hp,
        sec_add=sec_add,
        sec_area=sec_area
    )
    await database.execute(query)

    # 로그인 페이지로 리다이렉트
    return RedirectResponse(url="/login", status_code=303)
