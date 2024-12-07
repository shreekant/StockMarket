from flask import Flask, render_template, redirect, url_for
import subprocess
from flask_bootstrap import Bootstrap

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run-script')
def run_script():
    # Run the main.py script
    subprocess.run(['python', 'main.py'])
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
    # Add this line to enable the use of Bootstrap
    app.config['BOOTSTRAP_SERVE_LOCAL'] = True

    # Initialize Bootstrap
    Bootstrap(app)
