from django.shortcuts import render
from django.http import HttpResponse
from mainapp.models import Security
from mainapp.models import Post
from mainapp.main import sec
import datetime
from django.db.models import Max

from django.shortcuts import render
import cv2

# Create your views here.

### 메인 index 페이지 1~3
def index(request) :
    return render(request,
                  "mainapp/index.html",
                  {})
    
def index2(request) :
    return render(request,
                  "mainapp/index_2.html",
                  {})
    
def index3(request) :
    return render(request,
                  "mainapp/index_3.html",
                  {})
    
    
    

### 로그인    
def login_chk(request) :
    # - 아이디 및패스워드 전송받기
    sec_id = request.POST.get("sec_id", "")
    sec_pw = request.POST.get("sec_pw", "")
    
    sec_view = sec.getLoginChk(sec_id,sec_pw)
    
    if sec_view.get("result") == "None" :
        msg = """
            <script type='text/javascript'>
            alert('회원 정보가 일치하지 않습니다. 다시 입력해주세요!');
            location.href='/login/';
        </script>
        """
        return HttpResponse(msg)
    
    msg ="{}/ {}/ {}".format(sec_view["sec_id"],
                              sec_view["sec_pw"],
                              sec_view["sec_nm"])
    
    ### 로그인 인증처리하기 (세션처리하기)
    # - 조회결과가 있으면 세션객체에 회원정보를 담으면 끝~
    # - 세션객체는 딕셔너리 타입입니다.
    # - 세션객체에 값을 담는것은 딕셔너리에 값을 넣는것과 동일함
    request.session["ses_sec_id"] = sec_id
    request.session["ses_sec_nm"] = sec_view.get("sec_nm")
    
    ## 로그인 인증처리(세션처리) 후 페이지 링크 처리
    msg = """
        <script type='text/javascript'>
        alert('환영합니다.[{}] 님 로그인 되었습니다.');
        location.href='/';
        </script>
    """.format(sec_view.get("sec_nm"))
    
    return HttpResponse(msg)
### 로그아웃
def logout_chk(request) :
    msg ="logout.."
    
    ### 로그아웃 처리는 session 딕셔너리 key를 없애주면 됩니다.
    # - 딕셔너리에서 모든 정보를 삭제하는 함수 :flush()
    request.session.flush()
    msg = """
            <script type='text/javascript'>
            alert('로그아웃 되었습니다.');
            location.href = '/';
            </script>
    """
    return HttpResponse(msg)

def login_pg(request) :
    return render(request,
                  "mainapp/login.html",
                  {})
    

### 웹캠
def webcam(request):
    # 웹캠 캡처
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # OpenCV에서 이미지를 BGR에서 RGB로 변환
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # 이미지를 HTML 페이지에 렌더링하기 위해 Django context에 추가
        context = {'frame': frame}

        # index.html 템플릿 렌더링
        return render(request, 'index.html', context)

    cap.release()