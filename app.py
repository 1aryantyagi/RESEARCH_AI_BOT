from flask import Flask, render_template, request
from main import process_query

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    topic = request.form['topic']
    result = process_query(topic)
    return render_template('results.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)