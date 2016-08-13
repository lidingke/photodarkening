from flask_bootstrap import Bootstrap
from flask import Flask, render_template
import pdb
app = Flask(__name__)

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name = name)

if __name__ == '__main__':
    bootstrap = Bootstrap(app)
    # app.run(debug=True)
    pdb.set_trace()
    pass
