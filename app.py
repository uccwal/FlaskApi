from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# MySQL 데이터베이스 설정
# 'mysql://username:password@localhost/database_name'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://springstudent:springstudent@localhost:3306/sampledb'
db = SQLAlchemy(app)

# 모델 정의
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

# GET 요청을 처리하는 뷰 함수
@app.route('/get_users', methods=['GET'])
def get_users():
    # 데이터베이스에서 데이터를 가져옵니다.
    users = User.query.all()

    # 데이터를 JSON 형식으로 내보냅니다.
    user_list = [{'id': user.id, 'username': user.username} for user in users]
    return jsonify(user_list)

# POST 요청을 처리하는 뷰 함수 (데이터 삽입)
@app.route('/add_user', methods=['POST'])
def add_user():
    # POST 요청에서 데이터를 가져옵니다.
    data = request.get_json()  # JSON 데이터를 예상하는 경우

    # 데이터베이스에 데이터 추가
    new_user = User(username=data['username'])  # 새로운 사용자 객체 생성
    db.session.add(new_user)  # 데이터베이스 세션에 추가
    db.session.commit()  # 변경 사항을 저장

    response_data = {'message': '새로운 사용자가 추가되었습니다.', 'user_id': new_user.id}
    return jsonify(response_data), 201  # 201은 Created HTTP 응답 코드입니다.


# GET 샘플
@app.route('/receive_get', methods=['GET'])
def join_get():
    name_receive = request.args.get('name_give') #'name_give'라는 key값
    print(name_receive)

    return jsonify({'result':'success', 'msg': 'GET 요청!'})


# POST 샘플
@app.route('/receive_post', methods=['POST'])
def receive_post():
    # POST 요청에서 데이터를 가져옵니다.
    data = request.get_json()  # JSON 데이터를 예상하는 경우
    # data = request.form['key']  # 폼 데이터를 가져오는 경우

    # 데이터를 처리하고 응답을 반환합니다.
    response_data = {'message': 'POST 요청이 성공적으로 처리되었습니다.', 'data': data}
    return response_data, 200  # 200은 HTTP 응답 코드 OK를 나타냅니다.

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
