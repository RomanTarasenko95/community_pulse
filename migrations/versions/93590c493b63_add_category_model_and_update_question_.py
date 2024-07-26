from alembic import op
import sqlalchemy as sa

# Revision identifiers, used by Alembic.
revision = '93590c493b63'
down_revision = 'f441d4814da9'
branch_labels = None
depends_on = None


def upgrade():
    # Create table for categories
    op.create_table(
        'categories',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(length=255), nullable=False)
    )

    # Add category_id column to questions table
    with op.batch_alter_table('questions', schema=None) as batch_op:
        batch_op.add_column(sa.Column('category_id', sa.Integer, nullable=True))
        batch_op.create_foreign_key('fk_questions_category', 'categories', ['category_id'], ['id'])


def downgrade():
    # Remove the foreign key and category_id column from questions table
    with op.batch_alter_table('questions', schema=None) as batch_op:
        batch_op.drop_constraint('fk_questions_category', type_='foreignkey')
        batch_op.drop_column('category_id')

    # Drop the categories table
    op.drop_table('categories')
