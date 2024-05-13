from flask import Flask, jsonify
import subprocess

from api.routes import xdg_blueprint

app = Flask(__name__)

app.register_blueprint(xdg_blueprint)

if __name__ == '__main__':
    app.run()