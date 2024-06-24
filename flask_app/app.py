import os

from dotenv import load_dotenv
from flask import Flask, send_from_directory
from flask.helpers import get_root_path

from src.api.dataset_routes import dataset_blueprint
from src.api.base_routes import base_blueprint
from src.api.dnn_routes import dnn_blueprint
from src.api.lr_routes import lr_blueprint
from src.api.rand_forest_routes import rand_forest_blueprint
from src.api.svm_routes import svm_blueprint
from src.api.xgb_routes import xgb_blueprint

load_dotenv()

FLASK_DEBUG = os.getenv('FLASK_DEBUG', 0)
print(f"FLASK_DEBUG: {FLASK_DEBUG}")
app = Flask(__name__)
app.config['DEBUG'] = FLASK_DEBUG

app.config.update(
    TEMPLATES_AUTO_RELOAD=True,
)

print(get_root_path(''))
@app.route('/assets/<path:path>')
def send_report(path):
    return send_from_directory('templates/assets', path)


app.register_blueprint(base_blueprint)
app.register_blueprint(dataset_blueprint)
app.register_blueprint(xgb_blueprint)
app.register_blueprint(svm_blueprint)
app.register_blueprint(rand_forest_blueprint)
app.register_blueprint(dnn_blueprint)
app.register_blueprint(lr_blueprint)

if __name__ == '__main__':
    app.run()
else:
    gunicorn_app = app
