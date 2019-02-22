import boto3
from utils.config import ConfigMalakAI
from sklearn.externals import joblib
import pandas


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
            "id": "1",
            "radius_mean": str(df_data['radius_mean']),
            "texture_mean": str(df_data['texture_mean']),
            "perimeter_mean": str(df_data['perimeter_mean']),
            "area_mean": str(df_data['area_mean']),
            "smoothness_mean": str(df_data['smoothness_mean']),
            "compactness_mean": str(df_data['compactness_mean']),
            "concavity_mean": str(df_data['concavity_mean']),
            "concave points_mean": str(df_data['concave_points_mean']),
            "symmetry_mean": str(df_data['symmetry_mean']),
            "fractal_dimension_mean": str(df_data['fractal_dimension_mean']),
            "radius_se": str(df_data['radius_se']),
            "texture_se": str(df_data['texture_se']),
            "perimeter_se": str(df_data['perimeter_se']),
            "area_se": str(df_data['area_se']),
            "smoothness_se": str(df_data['smoothness_se']),
            "compactness_se": str(df_data['compactness_se']),
            "concavity_se": str(df_data['concavity_se']),
            "concave points_se": str(df_data['concave_points_se']),
            "symmetry_se": str(df_data['symmetry_se']),
            "fractal_dimension_se": str(df_data['fractal_dimension_se']),
            "radius_worst": str(df_data['radius_worst']),
            "texture_worst": str(df_data['texture_worst']),
            "perimeter_worst": str(df_data['perimeter_worst']),
            "area_worst": str(df_data['area_worst']),
            "smoothness_worst": str(df_data['smoothness_worst']),
            "compactness_worst": str(df_data['compactness_worst']),
            "concavity_worst": str(df_data['concavity_worst']),
            "concave points_worst": str(df_data['concave_points_worst']),
            "symmetry_worst": str(df_data['symmetry_worst']),
            "fractal_dimension_worst": str(df_data['fractal_dimension_worst']),
          },
        PredictEndpoint=endpoint
        )
        df_result = df_result.append({'id': '1',
                                      'prediction': response['Prediction']['predictedLabel'],
                                      'predicted_scores': response['Prediction']['predictedScores'][response['Prediction']['predictedLabel']]}, ignore_index=True)

    return df_result