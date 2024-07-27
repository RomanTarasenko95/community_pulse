from app.models.database import db
from app.models.category import Category


class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    category = db.relationship('Category', backref='questions', lazy=True)
    responses = db.relationship('Response', backref='question', lazy=True)

    def __repr__(self):
        return f'Question: {self.text}'

class Statistic(db.Model):
    __tablename__ = 'statistics'

    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), primary_key=True)
    agree_count = db.Column(db.Integer, nullable=False, default=0)
    disagree_count = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return f'Statistic for Question {self.question_id}: {self.agree_count} agree VS {self.disagree_count} disagree'
