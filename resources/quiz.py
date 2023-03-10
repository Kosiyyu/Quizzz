from flask_restful import Resource, reqparse
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models.answer import Answer
from models.question import Question
from models.quiz import Quiz

parser = reqparse.RequestParser()
parser.add_argument('name', type=str)
parser.add_argument('questions', type=list, location='json')


class QuizByIdAPI(Resource):
    def get(self, quiz_id):
        try:
            quiz = Quiz.query.filter_by(id=quiz_id).first()
            if quiz is None:
                return {'message': 'The requested resource could not be found for the provided ID.'}, 404, {
                    'Content-Type': 'application/json'}
        except SQLAlchemyError:
            return {
                       'message': 'An unexpected error occurred while processing the request. Please try again later.'}, 500, {
                       'Content-Type': 'application/json'}
        return quiz.to_dict(), 200, {'Content-Type': 'application/json'}

    def delete(self, quiz_id):
        try:
            quiz = Quiz.query.filter_by(id=quiz_id).first()
            if quiz is None:
                return {'message': 'The requested resource could not be found for the provided ID.'}, 404, {
                    'Content-Type': 'application/json'}
            db.session.delete(quiz)
            db.session.commit()
        except SQLAlchemyError:
            return {
                       'message': 'An unexpected error occurred while processing the request. Please try again later.'}, 500, {
                       'Content-Type': 'application/json'}
        return {'': ''}, 204, {'Content-Type': 'application/json'}


class QuizAPI(Resource):
    def get(self):
        try:
            quizzes = Quiz.query.all()
            if quizzes is None:
                return {'message': 'The requested resource could not be found for the provided ID.'}, 404, {
                    'Content-Type': 'application/json'}
        except SQLAlchemyError:
            return {
                       'message': 'An unexpected error occurred while processing the request. Please try again later.'}, 500, {
                       'Content-Type': 'application/json'}
        return [q.to_dict() for q in quizzes], 200, {'Content-Type': 'application/json'}

    # def post(self):
    #     try:
    #         args = parser.parse_args()
    #         if not 'name' in args or not args['name']:
    #             return {
    #                        'message': 'The request is missing the "name" field or it is empty. Please check the request and try again.'}, 400, {
    #                        'Content-Type': 'application/json'}
    #         if not all(key in args for key in ('name', 'questions')):
    #             return {
    #                        'message': 'The request is missing one or more required fields. Please check the request and try again.'}, 400, {
    #                        'Content-Type': 'application/json'}
    #
    #         for question in args['questions']:
    #             if not 'text' in question or not question['text']:
    #                 return {
    #                            'message': 'The request is missing the "text" field for one or more questions or it is empty. Please check the request and try again.'}, 400, {
    #                            'Content-Type': 'application/json'}
    #             correct_answers = [a for a in question['answers'] if a['correct'] == True]
    #             if len(correct_answers) != 1:
    #                 return {'message': 'Each question should have only one correct answer'}, 400, {
    #                     'Content-Type': 'application/json'}
    #             for a in question['answers']:
    #                 if not 'text' in a or not a['text']:
    #                     return {
    #                                'message': 'The request is missing the "text" field for one or more answers or it is empty. Please check the request and try again.'}, 400, {
    #                                'Content-Type': 'application/json'}
    #         quiz = Quiz(name=args['name'])
    #         db.session.add(quiz)
    #         db.session.commit()
    #     except SQLAlchemyError:
    #         return {
    #                    'message': 'An unexpected error occurred while processing the request. Please try again later.'}, 500, {
    #                    'Content-Type': 'application/json'}
    #     return {'message': 'Resource created successfully.'}, 201, {'Content-Type': 'application/json'}

    def post(self):
        try:
            args = parser.parse_args()
            if not 'name' in args or not args['name']:
                return {
                           'message': 'The request is missing the "name" field or it is empty. Please check the request and try again.'}, 400, {
                           'Content-Type': 'application/json'}
            if not all(key in args for key in ('name', 'questions')):
                return {
                           'message': 'The request is missing one or more required fields. Please check the request and try again.'}, 400, {
                           'Content-Type': 'application/json'}

            existing_quiz = Quiz.query.filter_by(name=args['name']).first()
            if existing_quiz:
                return {
                           'message': 'A quiz with this name already exists. Please choose a different name and try again.'}, 400, {
                           'Content-Type': 'application/json'}

            quiz = Quiz(name=args['name'])
            db.session.add(quiz)
            db.session.commit()

            for q in args['questions']:
                if not 'text' in q or not q['text']:
                    return {
                               'message': 'The request is missing the "text" field for one or more questions or it is empty. Please check the request and try again.'}, 400, {
                               'Content-Type': 'application/json'}
                correct_answers = [a for a in q['answers'] if a['correct'] == True]
                if len(correct_answers) != 1:
                    return {'message': 'Each question should have only one correct answer'}, 400, {
                        'Content-Type': 'application/json'}
                for a in q['answers']:
                    if not 'text' in a or not a['text']:
                        return {
                                   'message': 'The request is missing the "text" field for one or more answers or it is empty. Please check the request and try again.'}, 400, {
                                   'Content-Type': 'application/json'}

                question = Question(text=q['text'],
                                    points_per_correct_answer=q.get('points_per_correct_answer', 0),
                                    quiz_id=quiz.id)
                db.session.add(question)
                db.session.commit()
                for a in q['answers']:
                    answer = Answer(text=a['text'], correct=a['correct'], question_id=question.id)
                    db.session.add(answer)
                    db.session.commit()
        except SQLAlchemyError:
            return {
                       'message': 'An unexpected error occurred while processing the request. Please try again later.'}, 500, {
                       'Content-Type': 'application/json'}
        return {'message': 'Resource created successfully.'}, 201, {'Content-Type': 'application/json'}


class QuizByNameAPI(Resource):
    def get(self, quiz_name):
        try:
            quiz = Quiz.query.filter_by(name=quiz_name).first()
            if quiz is None:
                return {'message': 'The requested resource could not be found for the provided name.'}, 404, {
                    'Content-Type': 'application/json'}
        except SQLAlchemyError:
            return {
                       'message': 'An unexpected error occurred while processing the request. Please try again later.'}, 500, {
                       'Content-Type': 'application/json'}
        return quiz.to_dict(), 200, {'Content-Type': 'application/json'}
