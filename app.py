import os

# Set environment variables
os.environ['BACKEND_URL'] = 'http://localhost:8080'
os.environ['JWT_TOKEN'] = 'eyJhbGciOiJIUzM4NCJ9.eyJzdWIiOiJwYXJlbnQiLCJpYXQiOjE3NTE4NzU3NDYsImV4cCI6MTc1MjQ4MDU0Nn0.bUSa4QFNFMQdHS64KAV6qjuyBoEvnnx5IYvrSXQ_CzQbeEjtdE0jNS_3-fZPcJnD'

from flask import Flask

from tracking.interfaces.services import tracking_api
from shared.infrastructure.database import init_db

app = Flask(__name__)
app.register_blueprint(tracking_api)

first_request = True

@app.before_request
def setup():
    global first_request
    if first_request:
        first_request = False
        init_db()

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')

