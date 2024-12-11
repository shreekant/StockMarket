from flask import Flask, render_template, redirect, url_for, send_file, jsonify
import subprocess
from flask_bootstrap import Bootstrap
import os

app = Flask(__name__)

# Variable to track the script status
script_status = 'idle'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run-script')
def run_script():
    global script_status
    script_status = 'running'
    print('Script status set to running')
    # Run the main.py script
    subprocess.run(['python', 'main.py'])
    script_status = 'completed'
    print('Script status set to completed')
    return redirect(url_for('index'))

@app.route('/show-excel')
def show_excel():
    # Path to the Excel file
    excel_path = 'stock_details.xlsx'
    if os.path.exists(excel_path):
        return send_file(excel_path, as_attachment=True)
    else:
        return "Excel file not found", 404

@app.route('/check-status')
def check_status():
    global script_status
    return jsonify({'status': script_status})

if __name__ == '__main__':
    app.run(debug=True)
    # Add this line to enable the use of Bootstrap
    app.config['BOOTSTRAP_SERVE_LOCAL'] = True

    # Initialize Bootstrap
    Bootstrap(app)