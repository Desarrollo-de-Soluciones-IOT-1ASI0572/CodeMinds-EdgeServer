from flask import Flask
from shared.infrastructure.database import init_db
from iam.interfaces.services import iam_api

app = Flask(__name__)
app.register_blueprint(iam_api)

first_request = True

@app.before_request
def setup():
    global first_request
    if first_request:
        first_request = False
        init_db()

if __name__ == "__main__":
    app.run(debug=True)
