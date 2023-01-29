from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:3003@localhost:3306/iot'
db = SQLAlchemy(app)

@app.route('/', methods=['GET'])
def index():
    return "hello"

if __name__ == '__main__':
    app.run(debug=True)