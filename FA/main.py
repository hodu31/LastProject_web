### 필요 라이브러리 등
from fastapi import FastAPI, HTTPException, Form, Request,WebSocket
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse, Response, JSONResponse
from starlette.requests import Request
from sqlalchemy import  Column, String, MetaData, select, Integer, ForeignKey, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from databases import Database
from starlette.middleware.sessions import SessionMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.sql import func
import asyncio
from sqlalchemy import select,func


### 서버 실행 코드: uvicorn main:app --reload ###

# 로케이션 데이터베이스 연결 URL 설정
#DATABASE_URL = "mysql+pymysql://root:0000@127.0.0.1:3306/security"

# 서버 데이터베이스 연결 URL 설정
DATABASE_URL = "mysql+pymysql://admin:noticare@db-noticare.cvcrdfcptqp8.ap-northeast-2.rds.amazonaws.com:3306/security"

# 데이터베이스 객체 생성
database = Database(DATABASE_URL)
metadata = MetaData()

# FastAPI 앱 객체 생성
app = FastAPI()

# 'static' 디렉토리의 정적 파일을 '/static' 경로로 제공
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/bootstrap", StaticFiles(directory="bootstrap"), name="bootstrap")
app.mount("/css", StaticFiles(directory="css"), name="css")
app.mount("/js", StaticFiles(directory="js"), name="js")
app.mount("/templates", StaticFiles(directory="templates"), name="templates")
app.mount("/static/mainapp/aboutpage", StaticFiles(directory="static/mainapp/aboutpage"), name="aboutpage")


# 세션 미들웨어 추가 (사용자 세션 관리를 위함)
app.add_middleware(SessionMiddleware, secret_key="your-secret-key")

# Jinja2 템플릿 설정
templates = Jinja2Templates(directory="templates")

# SQLAlchemy의 기본 클래스 생성
Base = declarative_base()

    
# ls user 모델 정의
class LastproUser(Base):
    __tablename__ = "LASTPRO_USERS"
    USER_ID = Column(String(40), primary_key=True)
    USER_PW = Column(String(40))
    USER_NM = Column(String(15))
    USER_STORE = Column(String(20))
    USER_ADD = Column(String(30))
    USER_HP = Column(String(20))
    USER_ADD2 = Column(String(30))
    
# ls shop 모델 정의
class LastproShop(Base):
    __tablename__ = "LASTPRO_SHOP"
    SHOP_ID = Column(String(40), primary_key=True)
    USER_ID = Column(String(40), ForeignKey("LASTPRO_USERS.USER_ID"), primary_key=True)
   
# ls visit 모델 정의
class LastproVisit(Base):
    __tablename__ = "LASTPRO_VISIT"
    SHOP_ID = Column(String(40), ForeignKey("LASTPRO_SHOP.SHOP_ID"), primary_key=True)
    USER_ID = Column(String(40), ForeignKey("LASTPRO_USERS.USER_ID"), primary_key=True)
    V_ID = Column(String(50), primary_key=True)
    V_ENTIME = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    
    
# ls dancode 모델 정의
class LastproDanCode(Base):
    __tablename__ = "LASTPRO_DAN_CODE"
    DAN_CODE = Column(Integer, primary_key=True)
    DAN_CODE_KOR = Column(String(50))
    
# ls dan 모델 정의
class LastproDan(Base):
    __tablename__ = "LASTPRO_DAN"
    DAN_V_ID = Column(String(50),ForeignKey("LASTPRO_VISIT.V_ID"), primary_key=True)
    SHOP_ID = Column(String(40), ForeignKey("LASTPRO_SHOP.SHOP_ID"), primary_key=True)
    USER_ID = Column(String(40), ForeignKey("LASTPRO_USERS.USER_ID"), primary_key=True)
    DAN_CODE = Column(Integer, ForeignKey("LASTPRO_DAN_CODE.DAN_CODE"), primary_key=True)
    DAN_TIME = Column(TIMESTAMP,primary_key=True ,server_default=func.now(), nullable=False)

    
# 공통 로직을 위한 비동기 함수
async def get_common_data():
    # 사용자 정보 가져오기
    user_query = select(LastproUser)
    users = await database.fetch_all(user_query)

    # 상점 정보 가져오기
    shop_query = select(LastproShop)
    shops = await database.fetch_all(shop_query)

    # 방문자 정보 가져오기
    visit_query = select(LastproVisit)
    visits = await database.fetch_all(visit_query)

    # 행동 코드 정보 가져오기
    dancode_query = select(LastproDanCode)
    dancodes = await database.fetch_all(dancode_query)

    # 행동 정보 가져오기
    dan_query = select(LastproDan)
    dans = await database.fetch_all(dan_query)
  
    return users, shops, visits, dancodes, dans



@app.get("/get_dan_count")
async def get_dan_count():
    dan_query = select(LastproDan)
    dans = await database.fetch_all(dan_query)
    return {"dan_count": len(dans)}

@app.get("/get_visitor_count")
async def get_visitor_count():
    visit_query = select(LastproVisit)  # LastproVisit는 방문자 정보를 담고 있는 테이블이라고 가정합니다.
    visits = await database.fetch_all(visit_query)
    return {"visitor_count": len(visits)}

@app.get("/get_dan_count2")
async def get_dan_count2():
    dan_query = select(LastproDan).filter(LastproDan.DAN_CODE.in_([3, 4, 6, 7, 8]))
    dans2 = await database.fetch_all(dan_query)
    return {"dan_count2": len(dans2)}

@app.get("/get_monthly_visitors")
async def get_monthly_visitors():
    query = """
    SELECT DATE_FORMAT(V_ENTIME, '%Y-%m') as month, COUNT(*) as counts
    FROM LASTPRO_VISIT
    WHERE YEAR(V_ENTIME) = 2023
    GROUP BY month
    """
    result = await database.fetch_all(query)
    return {"monthly_visitors": result}

last_added_row_id = None

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    global last_added_row_id
    await websocket.accept()

    if last_added_row_id is None:
        initial_query = select(LastproDan).order_by(LastproDan.DAN_TIME.desc()).limit(1)
        last_added_row = await database.fetch_one(initial_query)
        last_added_row_id = last_added_row['DAN_TIME']

    while True:
        new_row_query = select(LastproDan).filter(LastproDan.DAN_TIME > last_added_row_id).order_by(LastproDan.DAN_TIME.asc())
        new_rows = await database.fetch_all(new_row_query)

        for row in new_rows:
            await websocket.send_json({"dan_code": row['DAN_CODE']})
            last_added_row_id = row['DAN_TIME']

        await asyncio.sleep(1)


# 모든 페이지에 대한 핸들러
@app.get("/{page}", response_class=HTMLResponse)
async def read_page(request: Request, page: str):
    if page == "favicon.ico":
        return Response(status_code=204)  # No Content
    else:
        # 세션에서 로그인 정보 가져오기
        user_id = request.session.get("user_id")
        user = None
        if user_id:
            query = select(LastproUser).where(LastproUser.USER_ID == user_id)
            user = await database.fetch_one(query)
      
        # 공통 데이터 가져오기
        users, shops, visits, dancodes, dans = await get_common_data()

        # 방문자 수를 사용자 수와 동일한 길이로 출력
        visitor_count = len(visits)  # 또는 다른 데이터를 사용하여 계산
        
        # 이상감지 수를 사용자 수와 동일한 길이로 출력
        dan_count = len(dans)  # 또는 다른 데이터를 사용하여 계산
        return templates.TemplateResponse(
            f"{page}.html", 
            {"request": request, "user": user, "users": users, "shops": shops, "visits": visits, "dancodes": dancodes, "dans": dans,
             "visitor_count":visitor_count, "dan_count":dan_count}
        )



@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return RedirectResponse(url="/static/mainapp/aboutpage/aboutus.html")


# index 경로에 대한 핸들러
@app.get("/index", response_class=HTMLResponse)
async def read_root(request: Request):
    user_id = request.session.get("user_id")
    user = None

    if user_id:
        query = select(LastproUser).where(LastproUser.USER_ID == user_id)
        user = await database.fetch_one(query)

    return templates.TemplateResponse("index.html", {"request": request, "user": user})


# index3 경로에 대한 핸들러
@app.get("/index3", response_class=HTMLResponse)
async def index3_page(request: Request):
    user_id = request.session.get("user_id")
    user = None
    if user_id:
        query = select(LastproUser).where(LastproUser.USER_ID == user_id)
        user = await database.fetch_one(query)
    return templates.TemplateResponse("index3.html", {"request": request, "user": user})



# 가입 페이지에 대한 핸들러
@app.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@app.post("/login/")
async def login(request: Request, USER_ID: str = Form(...), USER_PW: str = Form(...)):
    query = select(LastproUser).where(LastproUser.USER_ID == USER_ID)
    user = await database.fetch_one(query)
    if not user:
        return templates.TemplateResponse("login.html", {"request": request, "error": "입력한 ID 정보가 없습니다."})
    if user.USER_PW != USER_PW:
        return templates.TemplateResponse("login.html", {"request": request, "error": "패스워드가 잘못되었습니다."})
    
    request.session["user_id"] = USER_ID
    return RedirectResponse(url="/index", status_code=303)

@app.post("/reauthenticate/")
async def reauthenticate(request: Request, USER_PW: str = Form(...)):
    query = select(LastproUser).where(LastproUser.USER_PW == USER_PW)
    user = await database.fetch_one(query)
    if user is None:
        return JSONResponse(content={"success": False, "error": "패스워드가 잘못되었습니다."})
    
    request.session["user_pw"] = USER_PW
    return JSONResponse(content={"success": True})


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
    USER_ID: str = Form(...),
    USER_PW: str = Form(...),
    USER_NM: str = Form(...),
    USER_STORE: str = Form(...),
    USER_ADD: str = Form(...),
    USER_HP: str = Form(...),
    USER_ADD2: str = Form(...)
):
    # 이미 존재하는 사용자인지 확인
    query = select(LastproUser).where(LastproUser.USER_ID == USER_ID)
    user = await database.fetch_one(query)
    if user:
        raise HTTPException(status_code=400, detail="User ID already exists")

    # 사용자 정보 저장
    query = LastproUser.__table__.insert().values(
        USER_ID=USER_ID,
        USER_PW=USER_PW,
        USER_NM=USER_NM,
        USER_STORE=USER_STORE,
        USER_ADD=USER_ADD,
        USER_HP=USER_HP,
        USER_ADD2=USER_ADD2
    )
    await database.execute(query)

    # 로그인 페이지로 리다이렉트
    return RedirectResponse(url="/login", status_code=303)