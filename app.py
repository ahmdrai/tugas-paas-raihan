from flask import Flask, render_template, request, redirect, jsonify
from models import db, Expense
from dotenv import load_dotenv
import os
import time
from datetime import datetime
import shutil

load_dotenv()
app = Flask(__name__)

db_url = os.getenv("DATABASE_URL", "sqlite:///expenses.db")
if db_url.startswith("mysql://"):
    db_url = db_url.replace("mysql://", "mysql+pymysql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

db.init_app(app)
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/expenses')
def expenses():
    data = Expense.query.order_by(Expense.created_at.desc()).all()
    return render_template('expenses.html', expenses=data)

@app.route('/expenses/add', methods=['POST'])
def add_expense():
    title = request.form['title']
    amount = request.form['amount']
    category = request.form['category']
    created_at = datetime.strptime(
        request.form['created_at'],
        '%Y-%m-%d'
    ).date()
    expense = Expense(
        title=title,
        amount=float(amount),
        category=category,
        created_at=created_at
    )
    db.session.add(expense)
    db.session.commit()
    return redirect('/expenses')

@app.route('/expenses/delete/<int:id>', methods=['POST'])
def delete_expense(id):
    expense = Expense.query.get_or_404(id)
    db.session.delete(expense)
    db.session.commit()
    return redirect('/expenses')

@app.route('/summary')
def summary():
    expenses = Expense.query.all()
    total = sum(e.amount for e in expenses)
    count = len(expenses)
    return jsonify({
        "total_expense": total,
        "total_transactions": count
    })

@app.route('/expenses/<int:id>')
def expense_detail(id):
    expense = Expense.query.get_or_404(id)
    return render_template(
        'detail.html',
        expense=expense
    )

@app.route('/expenses/edit/<int:id>', methods=['GET', 'POST'])
def edit_expense(id):
    expense = Expense.query.get_or_404(id)
    if request.method == 'POST':
        expense.title = request.form['title']
        expense.amount = float(request.form['amount'])
        expense.category = request.form['category']
        expense.created_at = datetime.strptime(
            request.form['created_at'],
            '%Y-%m-%d'
        ).date()
        db.session.commit()
        return redirect('/expenses')
    return render_template(
        'edit.html',
        expense=expense
    )

@app.route('/health')
def health():
    start = time.time()
    try:
        db.session.execute(db.text('SELECT 1'))
        db_status = "connected"
    except:
        db_status = "disconnected"
    total, used, free = shutil.disk_usage("/")
    response_time = round((time.time() - start) * 1000, 2)
    return jsonify({
        "status": "healthy",
        "database": db_status,
        "disk_free_mb": round(free / (1024 * 1024), 2),
        "response_time_ms": response_time
    })

if __name__ == '__main__':
    app.run(debug=True)