from flask import Flask, request, jsonify
import json
from dao.model_data import ModelData
from utils.db.default_connector import DefaultConnector
from service.prediction import prediction
from utils.config import ConfigMalakAI
import pandas as pd
from random import randint

connector = DefaultConnector().get_default()
mocked_data = ConfigMalakAI().get('Settings', 'mocked_data', False)
app = Flask(__name__)

@app.route("/prediction", methods=['GET'])
def predict():
    '''
    Calculate the prediction
    '''

    if mocked_data:
        df_mocked = pd.read_csv('../data_files/mocked_data.csv', sep="|")
        num = randint(0, len(df_mocked)-1)
        data = df_mocked.iloc[num,:]
        result = prediction(data, local_train=True)
    else:
        data = json.loads(request.data)
        result = prediction(data)

    return jsonify(result.to_json(orient='records'))

@app.route("/init_database", methods=['GET'])
def init_database():
    connection = connector.create_connection()

    ModelData(connection).create()

    connection.commit_and_close()

    return jsonify({'result':'ok'})

if __name__ == "__main__":
    app.run(port=8080, debug=True)