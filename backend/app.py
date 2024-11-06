from flask import Flask, request, render_template, redirect, url_for
import os
import pandas as pd

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Replace with something secure

CSV_PATH = os.path.join(os.path.dirname(__file__), r'C:\Users\caden\Desktop\ScalpNetPrototype\data\options_data.csv')

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Here we can add a simple username/password verification (hardcoded for now)
        username = request.form['username']
        password = request.form['password']
        if username == "user" and password == "password":  # Replace with better auth in future
            return redirect(url_for('dashboard'))
        else:
            return "Invalid credentials. Please try again."

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    try:
        df = pd.read_csv(CSV_PATH)
        data = df.to_dict(orient='records')
        # Here we could add logic to pass the data to Plotly for visualization
        return render_template('dashboard.html', data=data)
    except Exception as e:
        return f"Error reading data: {e}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
