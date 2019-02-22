import boto3
from utils.config import ConfigMalakAI
from sklearn.externals import joblib
import pandas
import base64
import boto3
import json
import os

TRAINING_DATA_S3_URL = "s3://datos-cancer-hackathon-malakai-1/"
BUCKER_NAME = "datos-cancer-hackathon-malakai-1"

def prediction(df_data, default=True, model_id=None, endpoint=None, local_train=False):

    df_result = pandas.DataFrame(columns=['id','prediction','predicted_scores'])
    if local_train:
        load_model = joblib.load(ConfigMalakAI().get('ModelsSkleanr', 'default_local_model', ''))
        response = load_model.predict([[df_data['radius_mean'],
                                        df_data['texture_mean'],
                                        df_data['perimeter_mean'],
                                        df_data['area_mean'],
                                        df_data['smoothness_mean'],
                                        df_data['compactness_mean'],
                                        df_data['concavity_mean'],
                                        df_data['concave points_mean'],
                                        df_data['symmetry_mean'],
                                        df_data['fractal_dimension_mean'],
                                        df_data['radius_se'],
                                        df_data['texture_se'],
                                        df_data['perimeter_se'],
                                        df_data['area_se'],
                                        df_data['smoothness_se'],
                                        df_data['compactness_se'],
                                        df_data['concavity_se'],
                                        df_data['concave points_se'],
                                        df_data['symmetry_se'],
                                        df_data['fractal_dimension_se'],
                                        df_data['radius_worst'],
                                        df_data['texture_worst'],
                                        df_data['perimeter_worst'],
                                        df_data['area_worst'],
                                        df_data['smoothness_worst'],
                                        df_data['compactness_worst'],
                                        df_data['concavity_worst'],
                                        df_data['concave points_worst'],
                                        df_data['symmetry_worst'],
                                        df_data['fractal_dimension_worst']]])

        df_result = df_result.append({'id': df_data['id'],
                                      'prediction': response[0],
                                      'predicted_scores': None}, ignore_index=True)
    else:
        if default:
            model_id = ConfigMalakAI().get('Models', 'default', '')
            endpoint = ConfigMalakAI().get('EndPointsModels', 'default_endpoint', '')
        s3_client = boto3.client('machinelearning')
        response = s3_client.predict(
            MLModelId=model_id,
            Record={
            "id": str(df_data['id']),
            "radius_mean": str(df_data['radius_mean']),
            "texture_mean": str(df_data['texture_mean']),
            "perimeter_mean": str(df_data['perimeter_mean']),
            "area_mean": str(df_data['area_mean']),
            "smoothness_mean": str(df_data['smoothness_mean']),
            "compactness_mean": str(df_data['compactness_mean']),
            "concavity_mean": str(df_data['concavity_mean']),
            "concave points_mean": str(df_data['concave points_mean']),
            "symmetry_mean": str(df_data['symmetry_mean']),
            "fractal_dimension_mean": str(df_data['fractal_dimension_mean']),
            "radius_se": str(df_data['radius_se']),
            "texture_se": str(df_data['texture_se']),
            "perimeter_se": str(df_data['perimeter_se']),
            "area_se": str(df_data['area_se']),
            "smoothness_se": str(df_data['smoothness_se']),
            "compactness_se": str(df_data['compactness_se']),
            "concavity_se": str(df_data['concavity_se']),
            "concave points_se": str(df_data['concave points_se']),
            "symmetry_se": str(df_data['symmetry_se']),
            "fractal_dimension_se": str(df_data['fractal_dimension_se']),
            "radius_worst": str(df_data['radius_worst']),
            "texture_worst": str(df_data['texture_worst']),
            "perimeter_worst": str(df_data['perimeter_worst']),
            "area_worst": str(df_data['area_worst']),
            "smoothness_worst": str(df_data['smoothness_worst']),
            "compactness_worst": str(df_data['compactness_worst']),
            "concavity_worst": str(df_data['concavity_worst']),
            "concave points_worst": str(df_data['concave points_worst']),
            "symmetry_worst": str(df_data['symmetry_worst']),
            "fractal_dimension_worst": str(df_data['fractal_dimension_worst']),
          },
        PredictEndpoint=endpoint
        )
        df_result = df_result.append({'id': df_data['id'],
                                      'prediction': response['Prediction']['predictedLabel'],
                                      'predicted_scores': response['Prediction']['predictedScores'][response['Prediction']['predictedLabel']]}, ignore_index=True)

    return df_result



def build_model(data_s3_url, schema_fn, recipe_fn, name, train_percent=80):
    """Creates all the objects needed to build an ML Model & evaluate its quality.
    """
    ml = boto3.client('machinelearning')
    (train_ds_id, test_ds_id) = create_data_sources(ml, data_s3_url, schema_fn,
                                                    train_percent, name)

    ml_model_id = create_model(ml, train_ds_id, recipe_fn, name)
    eval_id = create_evaluation(ml, ml_model_id, test_ds_id, name)

    return ml_model_id


def create_data_sources(ml, data_s3_url, schema_fn, train_percent, name):
    """Create two data sources.  One with (train_percent)% of the data,
    which will be used for training.  The other one with the remainder of the data,
    which is commonly called the "test set" and will be used to evaluate the quality
    of the ML Model.
    """

    s3 = boto3.client('s3')

    filename = 'data501.csv'
    bucket_name = BUCKER_NAME

    # Uploads the given file using a managed uploader, which will split up large
    # files automatically and upload parts in parallel.
    s3.upload_file("C:/Users/Fran/Desktop/Pruebas/data.csv", bucket_name, filename)

    num_aleatorio = base64.b32encode(os.urandom(10))
    leerFichero = open(schema_fn).read()

    train_ds_id = 'ds-' + num_aleatorio.decode(encoding="utf8", errors="ignore")
    spec = {
        "DataLocationS3": data_s3_url,
        "DataRearrangement": json.dumps({
            "splitting": {
                "percentBegin": 0,
                "percentEnd": train_percent
            }
        }),
        "DataSchema": leerFichero,
    }
    ml.create_data_source_from_s3(
        DataSourceId=train_ds_id,
        DataSpec=spec,
        DataSourceName=name + " - training split",
        ComputeStatistics=True
    )
    print("Created training data set %s" % train_ds_id)

    num_aleatorio = base64.b32encode(os.urandom(10))
    test_ds_id = 'ds-' + num_aleatorio.decode(encoding="utf8", errors="ignore")
    spec['DataRearrangement'] = json.dumps({
        "splitting": {
            "percentBegin": train_percent,
            "percentEnd": 100
        }
    })
    ml.create_data_source_from_s3(
        DataSourceId=test_ds_id,
        DataSpec=spec,
        DataSourceName=name + " - testing split",
        ComputeStatistics=True
    )
    print("Created test data set %s" % test_ds_id)
    return (train_ds_id, test_ds_id)


def create_model(ml, train_ds_id, recipe_fn, name):
    """Creates an ML Model object, which begins the training process.
The quality of the model that the training algorithm produces depends
primarily on the data, but also on the hyper-parameters specified
in the parameters map, and the feature-processing recipe.
    """
    num_aleatorio = base64.b32encode(os.urandom(10))
    model_id = 'ml-' + num_aleatorio.decode(encoding="utf8", errors="ignore")
    leerFichero = open(recipe_fn).read()
    ml.create_ml_model(
        MLModelId=model_id,
        MLModelName=name + " model",
        MLModelType="MULTICLASS",  # we're predicting True/False values
        Parameters={
            # Refer to the "Machine Learning Concepts" documentation
            # for guidelines on tuning your model
            "sgd.maxPasses": "100",
            "sgd.maxMLModelSizeInBytes": "104857600",  # 100 MiB
            "sgd.l2RegularizationAmount": "1e-4",
        },
        Recipe=leerFichero,
        TrainingDataSourceId=train_ds_id
    )
    print("Created ML Model %s" % model_id)
    return model_id


def create_evaluation(ml, model_id, test_ds_id, name):
    num_aleatorio = base64.b32encode(os.urandom(10))
    eval_id = 'ev-' + num_aleatorio.decode(encoding="utf8", errors="ignore")
    ml.create_evaluation(
        EvaluationId=eval_id,
        EvaluationName=name + " evaluation",
        MLModelId=model_id,
        EvaluationDataSourceId=test_ds_id
    )
    print("Created Evaluation %s" % eval_id)
    return eval_id

def generar_datasource_model(ruta_fichero, nombre_machine_learning):
    try:
        data_s3_url = TRAINING_DATA_S3_URL
        schema_fn = "C:/Users/Fran/Desktop/Pruebas/breast.cancer.csv.schema"
        recipe_fn = "C:/Users/Fran/Desktop/Pruebas/recipe.json"
        name = nombre_machine_learning
    except:
        raise
    model_id = build_model(data_s3_url, schema_fn, recipe_fn, name=name)
