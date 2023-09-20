import cx_Oracle
import pandas as pd



### 회원 로그인 처리에 사용
def getLoginChk(sec_id,sec_pw):
    dsn = cx_Oracle.makedsn('localhost', 1521, 'xe')
    conn = cx_Oracle.connect('busan', 'dbdb', dsn)
    cursor = conn.cursor()
    
    sql = """
            select sec_id,sec_pw, sec_nm
            from security
            where sec_id = '{}'
            and sec_pw = '{}'
         """.format(sec_id,sec_pw)
    cursor.execute(sql)
    
    ### ('a001' , 'password' , '김은대')
    row = cursor.fetchone()
    
    ### 조회결과가 없으면,,, 아래 처리 안하고 return 시키기
    if row ==None :
        
        cursor.close()
        conn.close()
        return{"result" : "None"}
        
    ### 컬럼 데이터 추출하기
    colnames = cursor.description
    
    # 1. 컬럼을 리스트로 변경하기
    # 순수 for문으로만..
    cols = []
    for col in colnames:
        cols.append(col[0].lower())

    
    ### 딕셔너리 변환하기
    
    dict_row = {}
    for i in range(len(cols)) :
        dict_row[cols[i]] = row[i]
    
        
    cursor.close()
    conn.close()
    
    return dict_row