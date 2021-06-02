from flask import Flask

import auth
import events

app = Flask(__name__)

def create_app(app):
    app.register_blueprint(auth.mod)
    app.register_blueprint(events.mod)
    app.config.from_object(__name__)

create_app(app)

if __name__ == '__main__':
    app.run('localhost', 8001, debug=True)
