# Python libraries
import sys

# Find brain.
sys.path.insert(0, '..')

# Pip libraries
from flask import Flask, render_template

# Minion libraries
from brain_of_minion import find_files

app = Flask(__name__)

@app.route('/')
@app.route('/today')
@app.route('/next')
def today():
    context = {}
    context['files'] = ['Hello', 'World']
    context['files'] = find_files(
            filter = ['today'])
    return render_template('today.html', **context)

def render_minion_list(method):
    method = find_files
    return None

if __name__ == '__main__':
    app.run(debug=True)
