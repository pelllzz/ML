# 대문자, 소문자에 아주 민감하게 반응하니까 조심합시다
# 중간에 뭘 잘못 건드렸다 다시 올릴 때 서버가 "개복치"마냥 쓰러집니다

# Flask 라이브러리의 flask 클래스를 가져온다고 이해하면됨 (일단)
# 커스텀 모듈 불러올 때 (mod_sql 이런 거) main.py랑 같은 폴더에 있어야 안 터짐
# 자꾸 from 이런 거 왜 생기나 했더니 VS Code 자기가 알아서 패키지 끌어오고 있었어

from io import BytesIO

from pyrsistent import s
import mod_sql
import random
import pandas as pd
import numpy as np
#import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
from flask import Flask, render_template, request, send_file, url_for, redirect, jsonify, flash

# __name__ : 파일이름을 의미함
# 있어보이려고 한 건 아니고 파일이름이 아무리 바뀌어도 고정으로 들어갑니다
app = Flask(__name__)
app.secret_key = "Super Secret Key"

# Web => address(url), default -> localhost:5000
# / 뒤에 이렇다 할 URL 정보가 없으니 빈 URL이라고 칭하는 것이고 default는 위에 있는 것과 같다.
# 이거 그냥 쉽게 이해하려면 서버 올리고 처음 보이는 페이지인 index()에 접근한다고 보는 게 빠릅니다.
@app.route("/")

# 함수 이름은 그냥 알아서 지으면 되는데 중복만 안 되면 상관없습니다
def index():
    return render_template("index.html")

@app.route("/main3")
def main3():
    #sql = "SELECT name, position, introduce from team_pick"
    #_db = mod_sql.Database()
    #data = _db.execute_all(sql)
    return render_template('main3.html')

# localhost:5000/second 입력 시 second() 함수가 실행됩니다
@app.route("/second")
def second():
    return "Second Page"

@app.route("/third")
def third():
    return "Third Page"

@app.route("/login2")
def login2():
    _id = request.args.get("id")
    _pwd = request.args.get("password")
    #print(_id, _pwd) <- 이걸 request로 print하면 무슨 일이 벌어질까?
    if(_id == "test" and _pwd == "1234"):
        return "Welcome!!"
    else:   
        return "No No No"

@app.route("/signup/")
def signup():
    return render_template("signup.html")

# localhost:5000/signup2 요청이 들어오면 -> 형식이 POST인 경우 (default : GET)
@app.route("/signup2/", methods=["POST"])
def signup2():

    # signup 페이지에서 _id, _pwd, _name이 넘어 오는데 어떻게 처리할까
    # POST -> 데이터를 body 안에 담아서 요청함 / GET -> 데이터를 URL에 요청함 (What The...)
    # request.form은 딕셔너리 타입으로 넘어올 거고 우리가 입력한 데이터가 value, _id가 key 값이 될 것임

    if request.method=='POST':
        _id = request.form["_id"]

        print(_id)

        sql = '''SELECT id from team_pick WHERE id = "%s" ''' % (_id)
        _db = mod_sql.Database()
        data = _db.execute_all(sql)

        if data:
            print('USE OTHER ID')
            _db.close()
            flash('아이디가 중복되었습니다')
            return redirect(url_for('index'))

        else:
            _id = request.form["_id"]
            _pwd = request.form["_pwd"]
            _name = request.form["_name"]
            _position = request.form["_position"]
            
            # return _id, _pwd, _name : 터집니다 얘네 리턴하는게 왜..

            print(_id,_pwd,_name,_position) #이러면 서버 로그쪽에서 결과 확인이 가능합니다

            # connect DB

            sql = '''INSERT INTO team_pick VALUES (%s, %s, %s, %s, 0)'''
            values=[_id, _pwd, _name, _position]
            
            _db = mod_sql.Database() #mod_sql module class 선언
            _db.execute(sql, values)
            _db.commit()
            _db.close()
            flash('회원가입에 성공하였습니다')
            return redirect(url_for('index'))

            # redirect vs. render_template
            # render_template은 html 파일 그 자체를 불러오는 방식인 거고
            # redirect는 flask 안에 있는 함수를 가져오는 방식

            # 이제 SQL 에다가 데이터를 넣어봅시다. 당연히 SQL 테이블은 만들었겠지?

@app.route("/signin", methods=["POST"])
def signin():
    _id = request.form['_id']
    _pwd = request.form['_pwd']
    print(_id, _pwd)
    print(request.form)

    sql = '''SELECT id, pass from team_pick WHERE id = "%s" and pass = "%s" ''' % (_id, _pwd)
    _db = mod_sql.Database()
    data = _db.execute_all(sql)

    # SQL문 수행 시 회원이 아니라면 result 길이가 0이 될 테고 참이라면 결과는 1개만 나올 것임
    # 1개만 나온다고 -> id는 primary key = 중복불가능 -> 결과가 1개밖에 안 나오겠죠

    if data:
        # Login Success

        name=[]
        position=[]
        introduce=[]

        sqlb = '''SELECT `name`, `position`, `introduce` from team_pick'''
        _dbb = mod_sql.Database()
        datab = _dbb.execute_all(sqlb)

        for i in datab:
            name.append(i["name"])
            position.append(i["position"])
            introduce.append(i["introduce"])

        print(name)
        print(position)
        print(introduce)

        return render_template('main3.html', datab=datab, name=name, position=position, introduce=introduce)

    else:
        # Login Fail
        return redirect(url_for('index'))
    
    # return redirect(url_for('index'))

@app.route("/game", methods=["POST"])
def game():
    _use = request.form["_use"]

    # 가위바위보 진행시켜.... 랜덤 라이브러리 설치하고? 아니 import random
    list_ = ["가위", "바위", "보"]

    # 리스트 값 중에 하나 랜덤으로 뽑을겁니다
    choicelist = random.choice(list_)

    # 이제 if 문을 쓰면 되는데 귀찮아.....

    if _use == choicelist:
        return "무승부"
    elif _use == '가위':
        if choicelist == '바위' : return "패배!"
        else : return "승리!"
    elif _use == '바위':
        if choicelist == '보' : return "패배!"
        else : return "승리!"
    else:
        if choicelist == '가위' : return "패배!"
        else : return "승리!"


@app.route("/game2", methods=["POST"])
def game2():
    _use = request.form["use"]
    list_ = ['가위','바위','보']
    choicelist = random.choice(list_)

    if _use == choicelist:
        return jsonify({'result':"무승부"})
    if _use == '가위':
        if choicelist == '바위':
            return jsonify({'result':"패배"})
        else:
            return jsonify({'result':"승리"})
    if _use == '바위':
        if choicelist == '가위':
            return jsonify({'result':"패배"})
        else:
            return jsonify({'result':"승리"})
    if _use == '보':
        if choicelist == '바위':
            return jsonify({'result':"패배"})
        else:
            return jsonify({'result':"승리"})


# 이제 본격적으로 SQL이랑 그래프랑 별의 별 걸 다 섞어보는 시간
# csv 파일은 server 폴더 안에 넣어주세요
@app.route("/corona")
def corona():
    # 플라스크라고 다를 건 없음. 어차피 파이썬인데 뭐
    df = pd.read_csv('./csv/corona.csv')
    df.columns = ["인덱스","등록일시","사망자","확진자","게시글번호","기준일","기준시간","수정일시","누적의심자","누적확진률"]
    df.sort_values("등록일시", inplace=True)
    df["일일사망자"] = df["사망자"].diff().fillna(0)
    decide_data = df["일일사망자"].tolist()

    # 이제 그려야하는데 이미지 파일로 변경해서 띄울거임
    plt.plot(decide_data)
    img = BytesIO()
    plt.savefig(img, format='png', dpi=200)
    img.seek(0)

    # 이렇게 하면 그래프를 이미지 파일로 만든 거고 이걸 HTML 페이지에 띄워주는 것이 가능합니다
    return send_file(img, mimetype="image/png")

# 여기다가 그래프 띄울겁니다
@app.route("/graph")
def graph():
    # 어떻게 띄우는 지는 여기 HTML 파일 까보세요
    return render_template("graph.html")

@app.route("/chart")
def chart():
    
    df = pd.read_csv('./csv/corona.csv')
    df.columns = ["인덱스","등록일시","사망자","확진자","게시글번호","기준일","기준시간","수정일시","누적의심자","누적확진률"]
    df.sort_values("등록일시", inplace=True)
    df["일일사망자"] = df["사망자"].diff().fillna(0)
    decide_data = df["일일사망자"].tolist() # list => we got Y
    data_list = df["등록일시"].tolist() # list => we got X
    cnt = len(data_list)

    return render_template("dashboard.html", decide=decide_data, data_list=data_list, cnt=cnt)

    #chart.html에서 {% %} 이런식으로 파이썬 구문을 쓸 수가 있는데
    #len 이런 것도 안 먹습니다 당연히
    #리턴할 때 이것저것 다 만들어서 넘겨줘야 인식해요

    #그래프가 어떤 모양으로 나오는지 궁금하다면 이거만 확인해보셈
    #return render_template("chart.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

# 이제 응용단계
# SQL에서 데이터를 받아 그래프를 그리고 테이블을 뽑을겁니다

@app.route("/graph2")
def graph_2():
    ## sales Table : group by `Item Type`
    ## `Item Type`, `Units Sold`의 평균, 합계 총 3개 컬럼
    ## 일단 해보고 싶으면 try, finally 없이 시도해보고 나중에 넣어주셔요
    ## try / finally로 예외처리를 할건데 줄바꿈 조심하세요. 들여쓰기도 눈여겨 보시고.
    try:        
        sql = """
        select `Item Type`, SUM(`Units Sold`) as sum, AVG(`Units Sold`) as avg from sales
        group by `Item Type` order by `Item Type` desc
        """
        _db = mod_sql.Database()
        result = _db.execute_all(sql)
        #print("result =", result)

        # 리스트를 만들어서 각각 담을 거야
        item_type=[]
        sold_avg=[]
        sold_sum=[]

        for i in result:
            item_type.append(i["Item Type"])
            sold_avg.append(i["avg"])
            sold_sum.append(i["sum"])
        #print("item type=", item_type, "sold_avg=", sold_avg, "sold_sum=", sold_sum)

    finally:
        return render_template("dashboard2.html", t=result, x=item_type, y1=sold_avg, y2=sold_sum)
    
    # dashboard2.html -> t = 전체 데이터 값, x = 그래프 X축 값, y1&y2 = 그래프 Y축 값
    # 그래프는 t, x, y1, y2를 기준으로 데이터가 넘어갈 것임
    # 그러니까 t, x, y1, y2에 값만 잘 넣어주면 그래프는 무슨 식으로든 그려질 겁니다
    # chartjs를 집어넣었으니까 x, y1, y2를 기준으로 예쁘게 차트는 잘 그려줄 거임
    # 지금은 리스트가 3개니까 t도 컬럼이 3개인데... 이걸 테이블 컬럼의 개수와 상관없이 들어갈 수 있도록 할 수 있지 않을까?
    # t에 컬럼 개수와 상관없이 테이블이 완성되도록 해봅시다...

@app.route("/graph3")
def graph3():
    df = pd.read_csv("./csv/drinks.csv")
    
    # continent 컬럼에 결측치 존재함. 이 결측치를 'OT'로 변경해보세요.
    df['continent'] = df['continent'].fillna('OT')

    # grouping : continent => avg & sum : spirit_servings
    result = df.groupby('continent').spirit_servings.agg(['mean','sum'])

    result_x = result.index.tolist()
    result_y1 = result["mean"].tolist()
    result_y2 = result["sum"].tolist()

    print(result_x, result_y1, result_y2)

    result_dict = result.to_dict()
    print(result_dict)

    return render_template('dashboard4.html', t=result_dict, x=result_x, y1=result_y1, y2=result_y2)
    # dataframe에서 데이터를 보낼 때 데이터의 타입에 대한 부분을 봅시다

@app.route("/login/")
def login():
    return render_template("login.html")

@app.route("/dashboard3")
def dashboard3():
    try:        
        sql = """
        select `Item Type`, SUM(`Units Sold`) as sum, AVG(`Units Sold`) as avg from sales
        group by `Item Type` order by `Item Type` desc
        """
        _db = mod_sql.Database()
        result = _db.execute_all(sql)
        #result = eval(simplejson.dumps(_db.execute_all(sql)))
        print("result =", result)

        # 리스트를 만들어서 각각 담을 거야
        item_type=[]
        sold_avg=[]
        sold_sum=[]

        for i in result:
            item_type.append(i["Item Type"])
            sold_avg.append(i["avg"])
            sold_sum.append(i["sum"])
        print("item type=", item_type, "sold_avg=", sold_avg, "sold_sum=", sold_sum)

    finally:
        return render_template("dashboard3.html", t=result, x=item_type, y1=sold_avg, y2=sold_sum)

@app.route("/graph4")
def graph4():
    return render_template("graph4.html")

@app.route("/graph5")
def graph5():
    return render_template("graph5.html")

# Flask 가동!!
app.run