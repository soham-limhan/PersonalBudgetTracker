# 💎 Personal Budget Tracker

A beautiful, modern web application for tracking personal expenses and managing budgets with stunning iOS 26-style glassmorphism design.

![Version](https://img.shields.io/badge/version-2.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![Flask](https://img.shields.io/badge/flask-2.3+-red.svg)
![License](https://img.shields.io/badge/license-MIT-purple.svg)

## ✨ Features

### 💰 Expense Management
- **Add Transactions**: Track both expenses and credits (income)
- **Categorize Spending**: Organize transactions by custom categories
- **Transaction Notes**: Add detailed notes to each transaction
- **Quick Delete**: Remove transactions with one click
- **Real-time Updates**: See your spending data update instantly

### 📊 Budget Tracking
- **Monthly Budget**: Set and manage monthly spending limits
- **Budget Credits**: Add credits to your existing budget
- **Spending Overview**: View current month's expenses vs budget
- **Savings Summary**: See how much you've saved this month
- **Budget Alerts**: Visual indicators for budget status

### 📈 Data Visualization
- **Category Breakdown**: Interactive pie chart showing spending by category
- **Monthly Trends**: Line chart displaying expenses and credits over time
- **Budget Overview**: Doughnut chart showing budget utilization
- **Smart Analytics**: Automatic categorization and summaries

### 🔐 User Management
- **Secure Authentication**: Login and registration with password hashing
- **Password Reset**: Change your password from profile dropdown
- **Session Management**: Secure user sessions
- **Multi-user Support**: Each user has isolated data

### 🎨 Modern UI/UX
- **iOS 26 Glassmorphism**: Beautiful glass effects with backdrop blur
- **Vibrant Gradients**: Colorful animated buttons and backgrounds
- **Smooth Animations**: Micro-interactions throughout the app
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile
- **Dark Theme**: Eye-friendly gradient background
- **Emoji Icons**: Visual indicators for better UX

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone or download the repository**
   ```bash
   cd PersonalBudgetTracker
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python index.py
   ```

4. **Open your browser**
   Navigate to `http://localhost:5000`

---

## 📖 Usage Guide

### First Time Setup

1. **Register an Account**
   - Click on "✍️ Register" in the navbar
   - Enter a username and password
   - You'll be automatically logged in

2. **Set Your Monthly Budget**
   - On the dashboard, find the "📊 Monthly Budget" section
   - Enter your desired monthly budget amount
   - Click "💾 Save"

### Adding Transactions

1. **Navigate to the Dashboard**
2. **Fill out the transaction form**:
   - **Type**: Choose Expense (💸) or Credit (💵)
   - **Amount**: Enter the transaction amount
   - **Category**: Specify category (e.g., Food, Transport, Salary)
   - **Date**: Select transaction date (optional, defaults to today)
   - **Note**: Add any additional details (optional)
3. **Click "✨ Add Transaction"**

### Managing Your Budget

#### Set Budget
- Enter amount in "Set Budget" field
- Click "💾 Save"
- Your budget will be set for the current month

#### Add Credit to Budget
- Enter amount in "Add Credit" field
- Click "➕ Add"
- This will increase your current budget

### Resetting Your Password

1. **Click on your username** (👤) in the navbar
2. **Select "🔐 Reset Password"** from the dropdown
3. **Fill out the form**:
   - Enter current password
   - Enter new password
   - Confirm new password
4. **Click "✨ Update Password"**

### Viewing Analytics

The dashboard automatically displays:
- **Category Breakdown**: See which categories consume most of your budget
- **Monthly Trends**: Track your spending patterns over months
- **Budget Overview**: Visualize budget allocation
- **Savings Summary**: View detailed breakdown of current month

---

## 🎨 Design System

### Color Palette
- **Primary Purple**: `#667eea` → `#764ba2`
- **Secondary Pink**: `#f093fb` → `#f5576c`
- **Success Cyan**: `#4facfe` → `#00f2fe`
- **Danger Warm**: `#fa709a` → `#fee140`

### Typography
- **Font Family**: Inter (Google Fonts)
- **Weights**: 300, 400, 500, 600, 700

### Key Design Elements
- **Glassmorphism**: Semi-transparent cards with backdrop blur
- **Gradient Backgrounds**: Dynamic animated gradients
- **Floating Orbs**: Subtle background animations
- **Smooth Transitions**: 0.2s - 0.5s ease animations
- **Pill Buttons**: Fully rounded buttons with gradients

---

## 📁 Project Structure

```
PersonalBudgetTracker/
├── index.py                 # Main Flask application
├── data.json                # User data storage (auto-created)
├── requirements.txt         # Python dependencies
├── README.md               # This file
├── static/
│   ├── css/
│   │   └── style.css       # iOS 26 glassmorphism styles
│   └── js/
│       └── app.js          # Frontend JavaScript
└── templates/
    ├── base.html           # Base template with navbar
    ├── home.html           # Landing page
    ├── login.html          # Login page
    ├── register.html       # Registration page
    ├── dashboard.html      # Main dashboard
    └── reset_password.html # Password reset page
```

---

## 🔧 Technical Details

### Backend (Flask)
- **Framework**: Flask 2.3+
- **Security**: Werkzeug password hashing (PBKDF2-SHA256)
- **Data Storage**: JSON file-based database
- **Session Management**: Flask sessions with secret key

### Frontend
- **Charts**: Chart.js for data visualization
- **Styling**: Custom CSS with glassmorphism effects
- **Framework**: Bootstrap 5.3 (grid system and components)
- **Font**: Inter from Google Fonts
- **Icons**: Unicode emojis for better compatibility

### API Endpoints
- `GET /api/expenses` - Fetch user's expenses
- `GET /api/summary` - Get expense summary and analytics
- `GET /api/budget` - Get monthly budget
- `POST /api/budget` - Set or update budget
- `POST /add` - Add new transaction
- `POST /remove/<id>` - Remove transaction

---

## 🔒 Security Features

- **Password Hashing**: Werkzeug's `generate_password_hash` with PBKDF2-SHA256
- **Session Security**: Secure session management with Flask
- **Input Validation**: Server-side validation for all inputs
- **Password Requirements**: Minimum 4 characters (configurable)
- **Current Password Verification**: Required for password changes
- **User Data Isolation**: Each user's data is completely separate

---

## 🎯 Key Features Explained

### Transaction Types
- **Expense (💸)**: Deducts from your budget
- **Credit (💵)**: Adds to your budget (like salary, refunds)

### Budget Calculation
- **Net Spent** = Total Expenses - Total Credits
- **Remaining** = Monthly Budget - Net Spent
- **Savings** = Remaining (if positive)

### Data Visualization
1. **Category Chart**: Pie chart showing expenses and credits by category
2. **Monthly Trends**: Line chart comparing expenses vs credits over time
3. **Budget Chart**: Pie chart showing individual transactions vs remaining budget

---

## 🐛 Troubleshooting

### Port Already in Use
If port 5000 is in use, modify `index.py`:
```python
app.run(host='0.0.0.0', port=5001, debug=True)  # Change to 5001 or any available port
```

### Data File Issues
If `data.json` gets corrupted, simply delete it. A fresh file will be created on next run:
```bash
rm data.json  # or manually delete the file
```

### Browser Caching Issues
If styles don't update, hard refresh your browser:
- **Windows/Linux**: `Ctrl + Shift + R`
- **Mac**: `Cmd + Shift + R`

---

## 🚀 Future Enhancements

- [ ] Export data to CSV/Excel
- [ ] Recurring transactions
- [ ] Multiple budget periods (weekly, yearly)
- [ ] Email notifications for budget alerts
- [ ] Dark/Light theme toggle
- [ ] Data backup and restore
- [ ] Expense filtering and search
- [ ] Budget categories with individual limits
- [ ] Bill reminders
- [ ] Multi-currency support

---

## 📄 License

This project is available under the MIT License. Feel free to use, modify, and distribute as needed.

---

## 👨‍💻 Developer Notes

### Running in Production

For production deployment, consider:
1. Using a proper database (PostgreSQL, MySQL)
2. Setting a strong secret key via environment variable
3. Using a production WSGI server (Gunicorn, uWSGI)
4. Enabling HTTPS
5. Adding rate limiting
6. Implementing proper logging

### Environment Variables
```bash
export PBTV2_SECRET="your-secret-key-here"
```

### Development Mode
The app runs in debug mode by default. For production, set:
```python
app.run(host='0.0.0.0', port=5000, debug=False)
```

---

## 🙏 Acknowledgments

- **Chart.js** - Beautiful charts and graphs
- **Bootstrap** - Responsive grid system
- **Inter Font** - Modern, readable typography
- **Flask** - Lightweight Python web framework

---

## 📞 Support

For issues, questions, or suggestions:
1. Check the Troubleshooting section above
2. Review the Usage Guide
3. Check existing issues in the repository

---

**Built with ❤️ using Flask, Chart.js, and modern web technologies**

**Version 2.0** - iOS 26 Glassmorphism Edition
