from sqlalchemy import Table, Column, Float, String, Boolean
from dao.generic_dao import GenericDAO


class ModelData(GenericDAO):
    def __init__(self, conn):
        super().__init__(conn,
                         id_column='ID',
                         )
        self._table_name = "model_data"

        cols = [
            Column('id', Float),
            Column('diagnosis', String(2), key='diagnosis'),
            Column('radius_mean', Float, key='radius_mean'),
            Column('texture_mean', Float, key='texture_mean'),
            Column('perimeter_mean', Float, key='perimeter_mean'),
            Column('area_mean', Float, key='area_mean'),
            Column('smoothness_mean', Float, key='smoothness_mean'),
            Column('compactness_mean', Float, key='compactness_mean'),
            Column('concave points_mean', Float, key='concave_points_mean'),
            Column('symmetry_mean', Float, key='symmetry_mean'),
            Column('fractal_dimension_mean', Float, key='fractal_dimension_mean'),
            Column('radius_se', Float, key='radius_se'),
            Column('texture_se', Float, key='texture_se'),
            Column('perimeter_se', Float, key='perimeter_se'),
            Column('area_se', Float, key='area_se'),
            Column('smoothness_se', Float, key='smoothness_se'),
            Column('compactness_se', Float, key='compactness_se'),
            Column('concavity_se', Float, key='concavity_se'),
            Column('concave points_se', Float, key='concave_points_se'),
            Column('symmetry_se', Float, key='symmetry_se'),
            Column('fractal_dimension_se', Float, key='fractal_dimension_se'),
            Column('radius_worst', Float, key='radius_worst'),
            Column('texture_worst', Float, key='texture_worst'),
            Column('perimeter_worst', Float, key='perimeter_worst'),
            Column('area_worst', Float, key='area_worst'),
            Column('smoothness_worst', Float, key='smoothness_worst'),
            Column('compactness_worst', Float, key='compactness_worst'),
            Column('concavity_worst', Float, key='concavity_worst'),
            Column('concave points_worst', Float, key='concave_points_worst'),
            Column('symmetry_worst', Float, key='symmetry_worst'),
            Column('fractal_dimension_worst', Float, key='fractal_dimension_worst'),
            Column('predicted_scores', Float, key='predicted_scores'),
            Column('validate_prediction', Boolean, key='validate_prediction', default=True),
        ]

        self._table = Table(
            self._table_name,
            self.connector.get_metadata(),
            *cols,
            extend_existing=True
        )

    def get_all(self):
        self.select_all(use_bulk=True)