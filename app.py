import os

# Set environment variables
os.environ['BACKEND_URL'] = 'https://edugo-service-de983aa97099.herokuapp.com'
os.environ['JWT_TOKEN'] = 'eyJhbGciOiJIUzM4NCJ9.eyJzdWIiOiJwYXJlbnQiLCJpYXQiOjE3NTE5NDEyMTgsImV4cCI6MTc1MjU0NjAxOH0.Bm6Ej3IYgC10U5JWsY7nWhSE2NfE-RJliFGT48QaO4fiVuUyKB74svmn_pw1sdZb'

from flask import Flask

from tracking.interfaces.services import tracking_api
from iam.interfaces.services import iam_api
from assignments.interfaces.services import scan_api
from shared.infrastructure.database import init_db



app = Flask(__name__)
app.register_blueprint(tracking_api)
app.register_blueprint(iam_api)
app.register_blueprint(scan_api)

first_request = True

@app.before_request
def setup():
    global first_request
    if first_request:
        first_request = False
        init_db()


if __name__ == '__main__':
    app.run(debug=True, port=5000, host="0.0.0.0")