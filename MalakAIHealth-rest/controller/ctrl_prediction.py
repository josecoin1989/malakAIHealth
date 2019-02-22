from flask import Flask, request, jsonify
import json
from dao.model_data import ModelData
from utils.db.default_connector import DefaultConnector
from service.prediction import prediction
from utils.config import ConfigMalakAI
import pandas as pd
from random import randint
from flask_cors import CORS

connector = DefaultConnector().get_default()
mocked_data = ConfigMalakAI().get('Settings', 'mocked_data', False)
app = Flask(__name__)
CORS(app)

@app.route("/prediction", methods=['POST'])
def predict():
    '''
    Calculate the prediction
    '''

    if mocked_data is True:
        df_mocked = pd.read_csv('../data_files/mocked_data.csv', sep="|")
        num = randint(0, len(df_mocked)-1)
        data = df_mocked.iloc[num,:]
        result = prediction(data, local_train=True)
    else:
        try:
            data = json.loads(request.data.decode('utf-8'))

            if 'radius_mean' not in data or 'texture_mean' not in data or 'perimeter_mean' not in data \
                    or 'area_mean' not in data or 'smoothness_mean' not in data or 'compactness_mean' not in data \
                    or 'concavity_mean' not in data or 'concave_points_mean' not in data or 'symmetry_mean' not in data \
                    or 'fractal_dimension_mean' not in data or 'radius_se' not in data or 'texture_se' not in data \
                    or 'perimeter_se' not in data or 'area_se' not in data or 'smoothness_se' not in data \
                    or 'compactness_se' not in data or 'concavity_se' not in data or 'concave_points_se' not in data \
                    or 'symmetry_se' not in data or 'fractal_dimension_se' not in data or 'radius_worst' not in data \
                    or 'texture_worst' not in data or 'perimeter_worst' not in data or 'area_worst' not in data \
                    or 'smoothness_worst' not in data or 'compactness_worst' not in data or 'concavity_worst' not in data \
                    or 'concave_points_worst' not in data or 'symmetry_worst' not in data \
                    or 'fractal_dimension_worst' not in data:
                raise Exception("Not all the data informed")

            result = prediction(data)
        except Exception as e:
            return jsonify({'Eror':str(e)})
    return jsonify(result.to_json(orient='records'))

@app.route("/init_database", methods=['GET'])
def init_database():
    connection = connector.create_connection()

    ModelData(connection).create()

    connection.commit_and_close()

    return jsonify({'result':'ok'})

if __name__ == "__main__":
    app.run(port=8888, debug=True)