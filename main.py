from flask import Flask
from flask_cors import CORS
from flask_restful import Api

from config import DATABASE_CONFIG
from resources.answer import AnswerAPI, AnswerByIdAPI
from resources.question import QuestionAPI, QuestionByIdAPI
from resources.quiz import QuizAPI, QuizByIdAPI, QuizByNameAPI
from resources.result import ResultAPI, ResultByIdAPI

app = Flask(__name__)
CORS(app, supports_credentials=True)
db_url = f"{DATABASE_CONFIG['provider']}://{DATABASE_CONFIG['username']}:{DATABASE_CONFIG['password']}@{DATABASE_CONFIG['host']}:{DATABASE_CONFIG['port']}/{DATABASE_CONFIG['database']}"
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CORS_HEADERS'] = 'Content-Type'

with app.app_context():
    from db import db

    # init db
    db.init_app(app)
    # create-drop
    db.drop_all()
    db.create_all()

api = Api(app)

# !!!- - R O U T S - -!!!
api.add_resource(AnswerAPI, '/api/answers')
api.add_resource(AnswerByIdAPI, '/api/answers/id/<int:answer_id>')

api.add_resource(QuestionAPI, '/api/questions')
api.add_resource(QuestionByIdAPI, '/api/questions/id/<int:question_id>')

api.add_resource(QuizAPI, '/api/quizzes')
api.add_resource(QuizByIdAPI, '/api/quizzes/id/<int:quiz_id>')
api.add_resource(QuizByNameAPI, '/api/quizzes/name/<string:quiz_name>')

api.add_resource(ResultAPI, '/api/solve')
api.add_resource(ResultByIdAPI, '/api/solve/id/<int:result_id>')

if __name__ == '__main__':
    app.run(debug=True)
