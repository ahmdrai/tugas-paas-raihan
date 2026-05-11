# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

# Import datetime
from datetime import datetime

# Membuat instance database
db = SQLAlchemy()


# Model tabel Expense
class Expense(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(100),
        nullable=False
    )

    amount = db.Column(
        db.Float,
        nullable=False
    )

    category = db.Column(
        db.String(50),
        nullable=False
    )

    created_at = db.Column(
        db.Date,
        nullable=False
    )