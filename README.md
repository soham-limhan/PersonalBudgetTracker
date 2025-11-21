# Personal Budget Tracker (V2)

Simple Flask-based personal budget tracker that stores data in a local JSON file and provides visualization using Chart.js.

Prerequisites
- Python 3.8+
- Install dependencies (prefer a virtualenv)

On Windows PowerShell:

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Run the app:

```powershell
python index.py
```

Open http://127.0.0.1:5000 in your browser. Register a user, add expenses, and view charts on the dashboard.

Notes
- Data is stored locally in `data.json` in the project folder.
- This is a simple demo and not intended for production use. Secrets and password storage are minimal (passwords hashed, but sessions and secret key are development-grade). For production use, configure a real secret and stronger security.


-- by Soham Limhan
