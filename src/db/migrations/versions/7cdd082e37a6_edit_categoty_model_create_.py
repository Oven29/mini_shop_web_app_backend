"""Edit Categoty model: create subcategories; Edit Order Model: edit nullabling invoice_id

Revision ID: 7cdd082e37a6
Revises: b36d42bb4fef
Create Date: 2025-01-25 15:15:01.101356

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7cdd082e37a6'
down_revision: Union[str, None] = 'b36d42bb4fef'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('categories', schema=None) as batch_op:
        batch_op.add_column(sa.Column('parent_category_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'categories', ['parent_category_id'], ['id'])

    with op.batch_alter_table('orders', schema=None) as batch_op:
        batch_op.alter_column('invoice_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('orders', schema=None) as batch_op:
        batch_op.alter_column('invoice_id',
               existing_type=sa.INTEGER(),
               nullable=False)

    with op.batch_alter_table('categories', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('parent_category_id')

    # ### end Alembic commands ###
