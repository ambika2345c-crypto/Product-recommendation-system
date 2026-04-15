from flask import Flask, render_template, request
from model import recommend

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    recs = []

    if request.method == 'POST':
        user_id = request.form['user_id']
        recs = recommend(user_id)

    return render_template('index.html', recs=recs)

if __name__ == '__main__':
    app.run(debug=True)




