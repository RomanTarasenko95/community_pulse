from flask import Blueprint, request, jsonify
from app.models import Category, db
from app.schemas.questions import CategoryBase, CategoryResponse
from pydantic import ValidationError

categories_bp = Blueprint('categories', __name__, url_prefix='/categories')


@categories_bp.route('/', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    results = [CategoryResponse.from_orm(category).dict() for category in categories]
    return jsonify(results), 200


@categories_bp.route('/', methods=['POST'])
def create_category():
    data = request.get_json()
    try:
        category_data = CategoryBase(**data)
    except ValidationError as e:
        return jsonify(e.errors()), 400

    category = Category(name=category_data.name)
    db.session.add(category)
    db.session.commit()

    return jsonify(CategoryResponse.from_orm(category).dict()), 201


@categories_bp.route('/<int:category_id>', methods=['PUT'])
def update_category(category_id):
    category = Category.query.get(category_id)
    if category is None:
        return jsonify({'message': 'Category not found'}), 404

    data = request.get_json()
    if 'name' in data:
        category.name = data['name']
        db.session.commit()
        return jsonify(CategoryResponse.from_orm(category).dict()), 200
    else:
        return jsonify({'message': 'Missing data'}), 400


@categories_bp.route('/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    category = Category.query.get(category_id)
    if category is None:
        return jsonify({'message': 'Category not found'}), 404

    db.session.delete(category)
    db.session.commit()
    return jsonify({'message': f'Category {category_id} deleted'}), 200
