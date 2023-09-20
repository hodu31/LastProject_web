from django.db import models

## db에서 문자열을 관리하는 타입
from django.db.models.fields import CharField

## db에서 숫자값을 관리하는 타입
from django.db.models.fields import IntegerField  # IntegerField를 사용하기 위해 import

## db에서 데이트 타입 값을 관리하는 타입
from django.db.models.fields import DateField  # DateField를 사용하기 위해 import

from django.db.models.fields import TextField  # django.db.models.fields 모듈에서 TextField를 import

# Create your models here.


## 회원정보 테이블 매핑
class Security(models.Model) :
    sec_id = CharField(primary_key=True,
                       max_length=20, null=False)
    sec_pw = CharField(max_length=20, null=False)
    sec_nm = CharField(max_length=20, null=False)
    sec_bir = CharField(max_length=20, null=False)
    sec_add = CharField(max_length=100, null=False)
    sec_hp = CharField(max_length=20, null=False)
    sec_area = CharField(max_length=20, null=False)
    sec_reason = CharField(max_length=500, null=False)

    
    '''
    < 클래스가 만들어진 후 매핑 작업 수행하기>
        - python manage.py makemigrations oracleapp
        - python manage.py migrate
        - 최초 1번만 진행 : 이후 수정 후 그대로 사용 가능
        - 단 수정 후 변경이 안되는 경우에는 위의 매핑 작업 수행 필요
        - 그래도 안되면 pycache삭제 후 진행
    '''
    
    ## 내부클래스 정의 : 메타클래스
    class Meta :
        ## 실제 db의 테이블 이름 정의
        db_table = 'security'
        
        ## 사용한 app 이름 정의
        app_label = 'mainapp'
        
        ## 외부 DB에 테이블이 존재하는지 여부 
            ## 존재하면 False
            ## 존재하지 않으면 True
            ## DBMS와 같은 외부 DB와 연결할 때
                ## 일반적으로 db가 설계되어 만들어진 상태에서 사용되기 때문에
                ## False로 설정한 후 사용하는 것이 일반적
        managed = False
        
        
        
## 공지사항 테이블 매핑
class Post(models.Model) :
    post_id = CharField(primary_key=True,
                       max_length=20, null=False)
    post_no = IntegerField(max_length=5, null=False)
    post_date = DateField(null=False)
    post_title = CharField(max_length=100, null=False)
    post_content = CharField(max_length=500, null=False)

    
    '''
    < 클래스가 만들어진 후 매핑 작업 수행하기>
        - python manage.py makemigrations oracleapp
        - python manage.py migrate
        - 최초 1번만 진행 : 이후 수정 후 그대로 사용 가능
        - 단 수정 후 변경이 안되는 경우에는 위의 매핑 작업 수행 필요
        - 그래도 안되면 pycache삭제 후 진행
    '''
    
    ## 내부클래스 정의 : 메타클래스
    class Meta :
        ## 실제 db의 테이블 이름 정의
        db_table = 'post'
        
        ## 사용한 app 이름 정의
        app_label = 'mainapp'
        
        ## 외부 DB에 테이블이 존재하는지 여부 
            ## 존재하면 False
            ## 존재하지 않으면 True
            ## DBMS와 같은 외부 DB와 연결할 때
                ## 일반적으로 db가 설계되어 만들어진 상태에서 사용되기 때문에
                ## False로 설정한 후 사용하는 것이 일반적
        managed = False
        