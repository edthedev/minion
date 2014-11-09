from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def today():
    context = {}
    context['files'] = ['Hello', 'World']
    return render_template('today.html', **context)

if __name__ == '__main__':
    app.run(debug=True)
