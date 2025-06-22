from flask import Flask
from identity_assignment.interfaces.services import scan_api
from shared.infrastructure.database import init_db

app = Flask(__name__)
app.register_blueprint(scan_api)

first_request = True

@app.before_request
def setup():
    global first_request
    if first_request:
        first_request = False
        init_db()

if __name__ == '__main__':
    app.run(debug=True, port=5000)


