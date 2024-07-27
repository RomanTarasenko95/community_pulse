from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from app.models import Question, Category, db
from app.schemas.questions import QuestionCreate, QuestionResponse

questions_bp = Blueprint('questions', __name__, url_prefix='/questions')


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


@questions_bp.route('/', methods=['GET'])
def get_questions():
    questions = Question.query.all()
    results = [QuestionResponse.model_validate(question).model_dump() for question in questions]
    return jsonify(results), 200
