from flask import Blueprint, request, jsonify, make_response
from pydantic import ValidationError

from app.models import Question, db
from app.schemas.questions import QuestionCreate, QuestionResponse

questions_bp = Blueprint('questions', __name__, url_prefix='/questions')


# @questions_bp.route('/', methods=['GET'])
# def get_questions():
#     questions = Question.query.all()
#     questions_data = [{'id': q.id, 'text': q.text} for q in questions]
#     return jsonify(questions_data)


@questions_bp.route('/', methods=['GET'])
def get_questions():
    """Получение списка всех вопросов."""
    questions = Question.query.all()
    # Сериализуем объекты SQLAlchemy в Pydantic модели
    results = [QuestionResponse.from_orm(question).dict() for question in questions]
    return jsonify(results)


@questions_bp.route('/', methods=['POST'])
def create_question():
    data = request.get_json()

    try:
        question_data = QuestionCreate(**data)
    except ValidationError as e:
        return jsonify(e.errors()), 400

    # if not data or 'text' not in data:
    #     return jsonify({'error': 'Missing data'}), 400

    question = Question(text=data['text'])
    db.session.add(question)
    db.session.commit()

    return jsonify({'message': 'Question created', 'id': question.id}), 201


@questions_bp.route('/<int:question_id>', methods=['GET'])
def get_question(question_id):
    question = Question.query.get(question_id)

    if question is None:
        return jsonify({'message': 'Question with this ID not found'}), 404

    return jsonify({'id': f'{question.id}', 'message': f'{question.text}'}), 200


@questions_bp.route('/<int:question_id>', methods=['PUT'])
def update_question(question_id):
    question = Question.query.get(question_id)

    if question is None:
        return jsonify({'message': 'Question with this ID not found'}), 404

    data = request.get_json()
    if 'text' in data:
        question.text = data['text']
        db.session.commit()
        return jsonify({'message': 'Question updated'}), 200
    else:
        return jsonify({'message': 'Missing text'}), 400


@questions_bp.route('/<int:question_id>', methods=['DELETE'])
def delete_question(question_id):
    question = Question.query.get(question_id)

    if question is None:
        return jsonify({'message': 'Question with this ID not found'}), 404

    db.session.delete(question)
    db.session.commit()
    return jsonify({'message': f'Question {question.id} deleted'}), 200
