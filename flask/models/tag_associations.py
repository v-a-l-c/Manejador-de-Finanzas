from sqlalchemy import Table, Column, Integer, ForeignKey
from . import db

transaction_tag = Table(
    'transaction_tag', db.Model.metadata,
    Column('transaction_id', Integer, ForeignKey('transactions.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True)
)