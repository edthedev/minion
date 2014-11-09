# Python libraries
import sys
# import urllib

# Find brain.
sys.path.insert(0, '..')

# Pip libraries
from flask import Flask, render_template

# Minion libraries
from brain_of_minion import find_files

app = Flask(__name__)

@app.route('/file/')
def get_file():
    pass


def render_minion_files(method, **kwargs ):
    context = {}
    files = method(**kwargs)
    # url_files = [urllib.quote(item) for item in files ]
    context['files'] = files
    return render_template('today.html', **context)

@app.route('/')
@app.route('/today')
def today():
    return render_minion_files(
            find_files,
            filter = ['today']
            )

@app.route('/next')
def minion_next():
    return render_minion_files(
            find_files,
            filter = ['next']
            )

if __name__ == '__main__':
    app.run(debug=True)
