import json
from typing import List

from flask import Flask, request
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
api=Api(app)
# sqlite
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
# mysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:lian123456@localhost:3306/hogwarts'
db = SQLAlchemy(app)






app.config['db']=[]

@app.route('/')
def hello():
    return 'hello from ceshiren.com'


class TestCase(db.Model):
    __tablename__='testcase'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    decription = db.Column(db.String(120), nullable=True)
    steps=db.Column(db.String(1024), nullable=True)

    def __repr__(self):
        return '<TestCase %r>' % self.username

# option+enter快速倒入包
class TestCaseService(Resource):
    def get(self):
        """
        测试用例的浏览获取 /testcase.json /testcase.json?id=1
        """
        testcases: List[TestCase] =TestCase.query.all()
        res= [{
            'id': testcase.id,
            'name': testcase.name,
            'description': testcase.description,
            'steps': json.loads(testcase.steps)
        } for testcase in testcases]

        return {
            'body':res
        }
    def post(self):
        """
        上传用例，更新用例
        /testcase.json{'name':'xx',description':'xxx','steps':[]}
        """
        testcase=TestCase(
            name=request.json.get('name'),
            description=request.json.get('description'),
            steps=json.dumps(request.json.get('steps'))
        )
        db.session.add(testcase)
        db.session.commit()
        return 'ok'

class TaskService(Resource):
    def get(self):
        pass


class ReportService(Resource):
    def get(self):
        pass
api.add_resource(TestCaseService,'/testcase')
api.add_resource(TaskService,'/task')
api.add_resource(ReportService,'/report')

# 启动flask服务
if  __name__ == '__main__':
    app.run(debug=True)

#  关闭占用端口的进程
# 找到被占用的指定端口号所对应的进程信息并呈现，括号处填写对应要查找的端口号：sudo lsof -i:(port)
# 关闭这个进程：sudo kill (PID)

