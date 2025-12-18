from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import os
import json
import uuid
from datetime import datetime

APP_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(APP_DIR, 'data.json')

app = Flask(__name__)
app.secret_key = os.environ.get('PBTV2_SECRET') or 'dev-secret-change-me'


def init_db():
    if not os.path.exists(DB_PATH):
        with open(DB_PATH, 'w', encoding='utf-8') as f:
            json.dump({'users': {}}, f, indent=2)


def read_db():
    with open(DB_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


def write_db(db):
    with open(DB_PATH, 'w', encoding='utf-8') as f:
        json.dump(db, f, indent=2, ensure_ascii=False)


def create_user(username, password):
    db = read_db()
    if username in db['users']:
        return False, 'User already exists'
    db['users'][username] = {
        'password': generate_password_hash(password),
        'expenses': [],
        'monthly_budget': 0
    }
    write_db(db)
    return True, 'User created'


def set_monthly_budget(username, amount):
    db = read_db()
    user = db['users'].get(username)
    if user is None:
        return False
    try:
        user['monthly_budget'] = float(amount)
    except Exception:
        user['monthly_budget'] = 0
    write_db(db)
    return True


def get_monthly_budget(username):
    db = read_db()
    user = db['users'].get(username)
    if not user:
        return 0
    return float(user.get('monthly_budget', 0) or 0)


def verify_user(username, password):
    db = read_db()
    user = db['users'].get(username)
    if not user:
        return False
    return check_password_hash(user['password'], password)


def update_user_password(username, current_password, new_password):
    """Update user password after verifying current password"""
    db = read_db()
    user = db['users'].get(username)
    if not user:
        return False, 'User not found'
    # Verify current password
    if not check_password_hash(user['password'], current_password):
        return False, 'Current password is incorrect'
    # Update to new password
    user['password'] = generate_password_hash(new_password)
    write_db(db)
    return True, 'Password updated successfully'


def add_expense_for_user(username, amount, category, date_str=None, note='', tx_type='expense'):
    db = read_db()
    user = db['users'].get(username)
    if user is None:
        return False
    if date_str:
        try:
            date = datetime.fromisoformat(date_str).date()
        except Exception:
            date = datetime.utcnow().date()
    else:
        date = datetime.utcnow().date()
    expense = {
        'id': str(uuid.uuid4()),
        'amount': float(amount),
        'category': category,
        'date': date.isoformat(),
        'note': note,
        # default type is expense for backward compatibility
        'type': tx_type or 'expense'
    }
    user['expenses'].append(expense)
    write_db(db)
    return True


def remove_expense(username, expense_id):
    db = read_db()
    user = db['users'].get(username)
    if user is None:
        return False
    user['expenses'] = [e for e in user.get('expenses', []) if e['id'] != expense_id]
    write_db(db)
    return True


def get_expenses(username):
    db = read_db()
    user = db['users'].get(username)
    if not user:
        return []
    return sorted(user.get('expenses', []), key=lambda e: e['date'])


def summarize_expenses(username):
    expenses = get_expenses(username)
    by_category = {}
    by_category_credits = {}
    by_month = {}
    by_month_credits = {}
    for e in expenses:
        amt = float(e['amount'])
        cat = e.get('category', 'Other')
        # month key YYYY-MM
        m = e.get('date', '')[:7]
        if e.get('type') == 'credit':
            by_category_credits[cat] = by_category_credits.get(cat, 0) + amt
            if m:
                by_month_credits[m] = by_month_credits.get(m, 0) + amt
        else:
            by_category[cat] = by_category.get(cat, 0) + amt
            if m:
                by_month[m] = by_month.get(m, 0) + amt
    return {
        'by_category': by_category,
        'by_category_credits': by_category_credits,
        'by_month': by_month,
        'by_month_credits': by_month_credits
    }


@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return render_template('home.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        ok, msg = create_user(username, password)
        if ok:
            session['username'] = username
            return redirect(url_for('dashboard'))
        return render_template('register.html', error=msg)
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        if verify_user(username, password):
            session['username'] = username
            return redirect(url_for('dashboard'))
        return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))


@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        username = session['username']
        current_password = request.form.get('current_password', '')
        new_password = request.form.get('new_password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        # Validate inputs
        if not current_password or not new_password or not confirm_password:
            return render_template('reset_password.html', error='All fields are required')
        
        if new_password != confirm_password:
            return render_template('reset_password.html', error='New passwords do not match')
        
        if len(new_password) < 4:
            return render_template('reset_password.html', error='New password must be at least 4 characters')
        
        # Update password
        success, message = update_user_password(username, current_password, new_password)
        if success:
            return render_template('reset_password.html', success=message)
        else:
            return render_template('reset_password.html', error=message)
    
    return render_template('reset_password.html')


@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=session['username'])


@app.route('/add', methods=['POST'])
def add_expense():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    amount = request.form.get('amount')
    category = request.form.get('category', 'Other')
    date = request.form.get('date')
    note = request.form.get('note', '')
    tx_type = request.form.get('type', 'expense')
    try:
        add_expense_for_user(username, amount, category, date, note, tx_type)
    except Exception as e:
        return redirect(url_for('dashboard'))
    return redirect(url_for('dashboard'))


@app.route('/api/expenses')
def api_expenses():
    if 'username' not in session:
        return jsonify({'error': 'not logged in'}), 401
    username = session['username']
    return jsonify(get_expenses(username))


@app.route('/api/summary')
def api_summary():
    if 'username' not in session:
        return jsonify({'error': 'not logged in'}), 401
    username = session['username']
    summary = summarize_expenses(username)
    # compute current month spent and include budget info
    today = datetime.utcnow().date()
    current_month = today.strftime('%Y-%m')
    expenses_current = summary.get('by_month', {}).get(current_month, 0)
    credits_current = summary.get('by_month_credits', {}).get(current_month, 0)
    # net spent = expenses - credits
    net_spent = expenses_current - credits_current
    monthly_budget = get_monthly_budget(username)
    remaining = monthly_budget - net_spent
    summary.update({
        'current_month': current_month,
        'spent_current_month': net_spent,
        'expenses_current_month': expenses_current,
        'credits_current_month': credits_current,
        'monthly_budget': monthly_budget,
        'remaining': remaining
    })
    return jsonify(summary)


@app.route('/api/budget', methods=['GET', 'POST'])
def api_budget():
    if 'username' not in session:
        return jsonify({'error': 'not logged in'}), 401
    username = session['username']
    if request.method == 'GET':
        return jsonify({'monthly_budget': get_monthly_budget(username)})
    # POST: accept json or form
    data = request.get_json(silent=True) or request.form
    amount = data.get('amount') or data.get('budget') or data.get('monthly_budget')
    operation = data.get('operation', 'set')  # 'set' or 'add'
    if amount is None:
        return jsonify({'error': 'missing amount'}), 400
    try:
        if operation == 'add':
            # Add to existing budget
            current_budget = get_monthly_budget(username)
            new_budget = current_budget + float(amount)
            set_monthly_budget(username, new_budget)
        else:
            # Set/replace budget
            set_monthly_budget(username, amount)
    except Exception:
        return jsonify({'error': 'could not set budget'}), 500
    return jsonify({'monthly_budget': get_monthly_budget(username)})


@app.route('/remove/<expense_id>', methods=['POST'])
def remove_expense_route(expense_id):
    if 'username' not in session:
        return jsonify({'error': 'not logged in'}), 401
    username = session['username']
    try:
        remove_expense(username, expense_id)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
