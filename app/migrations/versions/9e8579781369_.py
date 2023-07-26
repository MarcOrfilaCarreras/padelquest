# -*- coding: utf-8 -*-
"""empty message

Revision ID: 9e8579781369
Revises: 
Create Date: 2023-07-26 20:55:21.524731

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '9e8579781369'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tournaments_results', schema=None) as batch_op:
        batch_op.alter_column('url_player1_couple1',
                              existing_type=mysql.VARCHAR(length=200),
                              nullable=True)
        batch_op.alter_column('url_player1_couple2',
                              existing_type=mysql.VARCHAR(length=200),
                              nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tournaments_results', schema=None) as batch_op:
        batch_op.alter_column('url_player1_couple2',
                              existing_type=mysql.VARCHAR(length=200),
                              nullable=False)
        batch_op.alter_column('url_player1_couple1',
                              existing_type=mysql.VARCHAR(length=200),
                              nullable=False)

    # ### end Alembic commands ###
