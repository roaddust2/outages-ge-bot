"""Change Chat model tg_chat_id type Int -> BigInt

Revision ID: da207b55b9c5
Revises: 14d6239d3c0a
Create Date: 2023-09-05 19:16:49.665357

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'da207b55b9c5'
down_revision = '14d6239d3c0a'
branch_labels = None
depends_on = None


def upgrade():
    # Change column type from Integer to BigInteger
    op.alter_column('chats', 'tg_chat_id', type_=sa.BigInteger)

def downgrade():
    # Change column type back to Integer if needed
    op.alter_column('chats', 'tg_chat_id', type_=sa.Integer)
