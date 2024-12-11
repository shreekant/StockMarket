from flask import Flask, render_template, redirect, url_for, send_file
import subprocess
from flask_bootstrap import Bootstrap
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run-script')
def run_script():
    # Run the main.py script
    subprocess.run(['python', 'main.py'])
    return redirect(url_for('index'))

@app.route('/show-excel')
def show_excel():
    # Path to the Excel file
    excel_path = 'stock_details.xlsx'
    if os.path.exists(excel_path):
        return send_file(excel_path, as_attachment=True)
    else:
        return "Excel file not found", 404

if __name__ == '__main__':
    app.run(debug=True)
    # Add this line to enable the use of Bootstrap
    app.config['BOOTSTRAP_SERVE_LOCAL'] = True

    # Initialize Bootstrap
    Bootstrap(app)
