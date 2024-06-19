from flask import Blueprint, jsonify, render_template, request

from src.api.controllers.lr_controller import lr_accuracy, lr_variable_importance_image, lr_variable_importance, \
    lr_break_down, lr_shapley, lr_ceteris_parabus, lr_model_performance, lr_pdp, lr_overview
from src.services.dataset_service import DatasetService
#lr = Logistic Regression
lr_blueprint = Blueprint('lr', __name__, url_prefix='/lr')


@lr_blueprint.route('/accuracy', methods=['GET'])
def get_accuracies():
    result = lr_accuracy()
    return (jsonify({'accuracy': result}))

@lr_blueprint.route('/vipimage', methods=['GET'])
def get_vip_image():
    result = lr_variable_importance_image()
    return jsonify({'vip': result})

@lr_blueprint.route('/vip', methods=['GET'])
def get_vip():
    result = lr_variable_importance()
    return result

@lr_blueprint.route('/breakdown', methods=['GET'])
def get_breakdown():
    input_parameters = request.args.to_dict()
    dataset_service = DatasetService()
    input_parameters['BMI'] = str(
        dataset_service.calculateBMI(input_parameters.get('weight'), input_parameters.get('height')))
    del input_parameters['weight']
    del input_parameters['height']
    result = lr_break_down(input_parameters)
    return result
@lr_blueprint.route('/shapley', methods=['GET'])
def get_shapley():
    input_parameters = request.args.to_dict()
    dataset_service = DatasetService()
    input_parameters['BMI'] = str(
        dataset_service.calculateBMI(input_parameters.get('weight'), input_parameters.get('height')))
    del input_parameters['weight']
    del input_parameters['height']
    result = lr_shapley(input_parameters)
    return result

@lr_blueprint.route('/overview', methods=['GET'])
def get_overview():
    input_parameters = request.args.to_dict()
    dataset_service = DatasetService()
    input_parameters['BMI']=str(dataset_service.calculateBMI(input_parameters.get('weight'),input_parameters.get('height')))
    del input_parameters['weight']
    del input_parameters['height']
    result = lr_overview(input_parameters)
    return result

@lr_blueprint.route('/ceterisparabus/<variable>/', methods=['GET'])
def get_ceterisparabus(variable):
    input_parameters = request.args.to_dict()
    result = lr_ceteris_parabus(input_parameters,variable)
    return render_template('plotly_chart.html', chart=result)
@lr_blueprint.route('/modelperformance', methods=['GET'])
def get_modelperformance():
    result = lr_model_performance()
    return render_template('plotly_chart.html', chart=result)

@lr_blueprint.route('/pdp/<variable>/', methods=['GET'])
def get_pdp(variable):
    result = lr_pdp(variable)
    return result

