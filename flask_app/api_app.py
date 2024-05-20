from flask import Flask

from flask_app.api.base_routes import base_blueprint
from flask_app.api.xdg_routes import xdg_blueprint

app = Flask(__name__)

app.register_blueprint(base_blueprint)
app.register_blueprint(xdg_blueprint)

if __name__ == '__main__':
    app.run()