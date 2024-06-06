from flask import Flask, send_from_directory

from api.base_routes import base_blueprint
from api.xdg_routes import xdg_blueprint

app = Flask(__name__)

app.config.update(
    TEMPLATES_AUTO_RELOAD=True,
)

@app.route('/assets/<path:path>')
def send_report(path):
    return send_from_directory('templates/assets', path)

app.register_blueprint(base_blueprint)
app.register_blueprint(xdg_blueprint)

if __name__ == '__main__':
    app.run()