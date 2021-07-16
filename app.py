from flask import Flask, Blueprint, jsonify, request, render_template
from flask_cors import CORS
from flask_restx import Api

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from apis import  email_to_calendar

app = Flask(__name__)

app.config.from_object(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/main', methods=['POST'])
def main_event():
  if request.method == 'POST':
    email_to_calendar.check_mail()
    return 'success'

api_bp = Blueprint("api", __name__, url_prefix="/auto/api/v1")
api = Api(api_bp, version='1.0', title='API', description='Automatic API', doc='/docs')

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=5000, debug=True)

    

