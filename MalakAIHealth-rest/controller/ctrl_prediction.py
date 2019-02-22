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
        data = json.loads(request.data.decode('utf-8'))

        result = prediction(data)

    return jsonify(result.to_json(orient='records'))

@app.route("/init_database", methods=['GET'])
def init_database():
    connection = connector.create_connection()

    ModelData(connection).create()

    connection.commit_and_close()

    return jsonify({'result':'ok'})

if __name__ == "__main__":
    app.run(port=8888, debug=True)