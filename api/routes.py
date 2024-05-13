import subprocess

from flask import Blueprint, jsonify, render_template

from api.controllers.xdg_controller import xdg_accuracy, xdg_variable_importance_image, xdg_variable_importance, \
    xdg_break_down, xdg_shapley, xdg_ceteris_parabus, xdg_model_performance, xdg_pdp

xdg_blueprint = Blueprint('xdg', __name__)


@xdg_blueprint.route('/date', methods=['GET'])
def get_date():
    result = subprocess.check_output(['date']).decode('utf-8')
    return jsonify({'date': result.strip()})

@xdg_blueprint.route('/cal', methods=['GET'])
def get_cal():
    result = subprocess.check_output(['cal']).decode('utf-8')
    return jsonify({'calendar': result.strip()})

@xdg_blueprint.route('/docker', methods=['GET'])
def get_docker():
    result = subprocess.check_output(['docker', 'ps']).decode('utf-8')
    return jsonify({'docker': result.strip()})

@xdg_blueprint.route('/cls', methods=['GET'])
def get_cls():
    result = subprocess.check_output(['cls']).decode('utf-8')
    return (jsonify({'cls': result.strip()}))
            
@xdg_blueprint.route('/accuracy', methods=['GET'])
def get_accuracies():
    result = xdg_accuracy()
    return (jsonify({'accuracy': result}))

@xdg_blueprint.route('/vipimage', methods=['GET'])
def get_vip_image():
    result = xdg_variable_importance_image()
    return jsonify({'vip': result})

@xdg_blueprint.route('/vip', methods=['GET'])
def get_vip():
    result = xdg_variable_importance()
    return render_template('plotly_chart.html', chart=result)
@xdg_blueprint.route('/breakdown', methods=['GET'])
def get_breakdown():
    result = xdg_break_down()
    return render_template('plotly_chart.html', chart=result)
@xdg_blueprint.route('/shapley', methods=['GET'])
def get_shapley():
    result = xdg_shapley()
    return render_template('plotly_chart.html', chart=result)
@xdg_blueprint.route('/ceterisparabus', methods=['GET'])
def get_ceterisparabus():
    result = xdg_ceteris_parabus()
    return render_template('plotly_chart.html', chart=result)
@xdg_blueprint.route('/modelperformance', methods=['GET'])
def get_modelperformance():
    result = xdg_model_performance()
    return render_template('plotly_chart.html', chart=result)

@xdg_blueprint.route('/pdp', methods=['GET'])
def get_pdp():
    result = xdg_pdp()
    return render_template('plotly_chart.html', chart=result)

