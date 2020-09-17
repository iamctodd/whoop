# Created on 18 Sep 2020

import unittest

import numpy as np
import pandas as pd
from pandas import Timestamp

from development.exploratory_analysis import clean_input_whoop_data


class TestExploratoryAnalysis(unittest.TestCase):
    def test_clean_whoop_data(self):
        sample_input_df = pd.DataFrame(
            {'source': np.repeat('whoop', 5),
             'date': np.repeat('2020-03-14', 5),
             'field': ['whoop_strain_maxhr', 'whoop_workout_duration', 'whoop_workout_count',
                       'whoop_strain_avghr', 'whoop_strain_score'],
             'value': [161, 134.7, 3.0, 84.0, 12.160080470759699]
             })

        pd.testing.assert_frame_equal(
            clean_input_whoop_data(input_data=sample_input_df,
                                   is_flat_file=True),
            pd.DataFrame(
                {'date': {0: Timestamp('2020-03-14 00:00:00'),
                          1: Timestamp('2020-03-14 00:00:00'),
                          2: Timestamp('2020-03-14 00:00:00'),
                          3: Timestamp('2020-03-14 00:00:00'),
                          4: Timestamp('2020-03-14 00:00:00')},
                 'field': {0: 'strain_maxhr',
                           1: 'workout_duration',
                           2: 'workout_count',
                           3: 'strain_avghr',
                           4: 'strain_score'},
                 'value': {0: 161.0, 1: 134.7, 2: 3.0, 3: 84.0, 4: 12.160080470759699}
                 }
            ),
            "Data doesn't appear to have been cleaned properly"
        )


if __name__ == '__main__':
    unittest.main()
