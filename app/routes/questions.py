from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from app.models import Question, Category, db
from app.schemas.questions import QuestionCreate, QuestionResponse

questions_bp = Blueprint('questions', __name__, url_prefix='/questions')


@questions_bp.route('/<int:question_id>', methods=['GET'])
def get_question(question_id):
    question = Question.query.get(question_id)
    if question is None:
        return jsonify({'message': 'Question not found'}), 404

    result = QuestionResponse.from_orm(question).dict()
    return jsonify(result), 200


@questions_bp.route('/', methods=['POST'])
def create_question():
    data = request.get_json()
    try:
        question_data = QuestionCreate.model_validate(data)
    except ValidationError as e:
        return jsonify(e.errors()), 400

    category = Category.query.get(question_data.category_id)
    if not category:
        return jsonify({'message': 'Category not found'}), 404

    question = Question(text=question_data.text, category_id=question_data.category_id)
    db.session.add(question)
    db.session.commit()
    return jsonify({'message': 'Question created', 'id': question.id}), 201


@questions_bp.route('/<int:question_id>', methods=['PUT'])
def update_question(question_id):
    question = Question.query.get(question_id)
    if question is None:
        return jsonify({'message': 'Question not found'}), 404

    data = request.get_json()
    if 'text' in data:
        question.text = data['text']
    if 'category_id' in data:
        category = Category.query.get(data['category_id'])
        if not category:
            return jsonify({'message': 'Category not found'}), 404
        question.category_id = data['category_id']

    db.session.commit()
    return jsonify(QuestionResponse.from_orm(question).dict()), 200


@questions_bp.route('/<int:question_id>', methods=['DELETE'])
def delete_question(question_id):
    question = Question.query.get(question_id)
    if question is None:
        return jsonify({'message': 'Question not found'}), 404

    db.session.delete(question)
    db.session.commit()
    return jsonify({'message': f'Question {question_id} deleted'}), 200


@questions_bp.route('/', methods=['GET'])
def get_questions():
    questions = Question.query.all()
    results = [QuestionResponse.from_orm(question).dict() for question in questions]
    return jsonify(results), 200
