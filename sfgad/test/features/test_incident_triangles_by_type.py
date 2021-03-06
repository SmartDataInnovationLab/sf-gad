from unittest import TestCase

import pandas as pd
from pandas.util.testing import assert_frame_equal, assert_series_equal

from sfgad.modules.features.incident_triangles_by_type import IncidentTrianglesByType


class TestIncidentTrianglesByType(TestCase):
    def setUp(self):
        # 1. time step
        self.df_1 = pd.DataFrame({'TIMESTAMP': ['2018-01-01 00:00:00', '2018-01-01 00:00:01', '2018-01-01 00:00:05',
                                                '2018-01-01 00:00:06', '2018-01-01 00:00:09'],
                                  'E_TYPE': ['LIKE', 'LIKE', 'MESSAGE', 'MESSAGE', 'LIKE'],
                                  'SRC_NAME': ['A', 'A', 'B', 'C', 'B'],
                                  'SRC_TYPE': ['NODE', 'NODE', 'NODE', 'NODE', 'NODE'],
                                  'DST_NAME': ['B', 'C', 'C', 'B', 'C'],
                                  'DST_TYPE': ['NODE', 'NODE', 'NODE', 'NODE', 'NODE']})
        self.df_1['TIMESTAMP'] = pd.to_datetime(self.df_1['TIMESTAMP'])

        # 2. time step
        self.df_2 = pd.DataFrame({'TIMESTAMP': ['2018-01-01 00:00:11', '2018-01-01 00:00:14', '2018-01-01 00:00:16',
                                                '2018-01-01 00:00:18', '2018-01-01 00:00:18'],
                                  'E_TYPE': ['MESSAGE', 'MESSAGE', 'LIKE', 'LIKE', 'MESSAGE'],
                                  'SRC_NAME': ['A', 'A', 'D', 'D', 'C'],
                                  'SRC_TYPE': ['NODE', 'NODE', 'NODE', 'NODE', 'NODE'],
                                  'DST_NAME': ['B', 'C', 'A', 'B', 'D'],
                                  'DST_TYPE': ['NODE', 'NODE', 'NODE', 'NODE', 'NODE']})
        self.df_2['TIMESTAMP'] = pd.to_datetime(self.df_2['TIMESTAMP'])

        # the target output of the feature after 1. (2.) time step
        self.target_df_1 = pd.DataFrame(
            data={'name': ['A', 'B', 'C'],
                  'IncidentTrianglesByLIKE': [1, 1, 1],
                  'IncidentTrianglesByMESSAGE': [2, 0, 0],
                  'IncidentTrianglesByFRIENDSHIP': [0, 0, 0]},
            columns=['name', 'IncidentTrianglesByLIKE', 'IncidentTrianglesByMESSAGE', 'IncidentTrianglesByFRIENDSHIP'])

        self.target_df_2 = pd.DataFrame(
            data={'name': ['A', 'B', 'C', 'D'],
                  'IncidentTrianglesByLIKE': [1, 1, 1, 0],
                  'IncidentTrianglesByMESSAGE': [1, 0, 0, 2],
                  'IncidentTrianglesByFRIENDSHIP': [0, 0, 0, 0]},
            columns=['name', 'IncidentTrianglesByLIKE', 'IncidentTrianglesByMESSAGE', 'IncidentTrianglesByFRIENDSHIP'])

        self.feature = IncidentTrianglesByType(edge_types=['LIKE', 'MESSAGE', 'FRIENDSHIP'])

    def test_init(self):
        self.assertEqual(self.feature.names, ['IncidentTrianglesByLIKE', 'IncidentTrianglesByMESSAGE',
                                              'IncidentTrianglesByFRIENDSHIP'])
        self.assertEqual(self.feature.ids, {})
        self.assertEqual(self.feature.inv_ids, {})
        self.assertEqual(self.feature.node_count, 0)
        self.assertEqual(self.feature.edges, {})
        self.assertEqual(self.feature.neighbors, {})

    def test_reset_after_processing(self):
        # process a time step
        self.feature.process_vertices(self.df_1, 1)

        # test resetting of the dictionaries
        self.assertEqual(self.feature.ids, {})
        self.assertEqual(self.feature.inv_ids, {})
        self.assertEqual(self.feature.node_count, 0)
        self.assertEqual(self.feature.edges, {})
        self.assertEqual(self.feature.neighbors, {})

    def test_result_df_shape(self):
        result_df_1 = self.feature.process_vertices(self.df_1, 1)

        self.assertEqual(result_df_1.shape, self.target_df_1.shape)

    def test_result_df_columns(self):
        result_df_1 = self.feature.process_vertices(self.df_1, 1)

        self.assertEqual(result_df_1.columns.tolist(), ['name', 'IncidentTrianglesByLIKE', 'IncidentTrianglesByMESSAGE',
                                                        'IncidentTrianglesByFRIENDSHIP'])

    def test_result_df_dtypes(self):
        result_df_1 = self.feature.process_vertices(self.df_1, 1)

        assert_series_equal(result_df_1.dtypes, self.target_df_1.dtypes)

    def test_result_df_values(self):
        result_df_1 = self.feature.process_vertices(self.df_1, 1)

        assert_series_equal(result_df_1['name'], self.target_df_1['name'])
        assert_series_equal(result_df_1['IncidentTrianglesByLIKE'], self.target_df_1['IncidentTrianglesByLIKE'])
        assert_series_equal(result_df_1['IncidentTrianglesByMESSAGE'], self.target_df_1['IncidentTrianglesByMESSAGE'])
        assert_series_equal(result_df_1['IncidentTrianglesByFRIENDSHIP'],
                            self.target_df_1['IncidentTrianglesByFRIENDSHIP'])

    def test_overall_processing_all_nodes(self):
        # test the calculation of two-hop reach in the 1. time step ('df_1')
        assert_frame_equal(self.feature.process_vertices(self.df_1, 1), self.target_df_1)

        # test the calculation of two-hop reach in the 2. time step ('df_2')
        assert_frame_equal(self.feature.process_vertices(self.df_2, 1), self.target_df_2)

    def test_interpret_edge(self):
        # add a new edge and verify the changes in neighbors-dictionary
        self.feature.register_node("A", 0)
        self.feature.register_node("B", 1)
        self.feature.interpret_edge("B", "A", "MESSAGE")
        self.feature.interpret_edge("A", "B", "LIKE")

        # test the neighbors update
        self.assertEqual(self.feature.neighbors[0], [1])
        self.assertEqual(self.feature.neighbors[1], [0])

        # test the edges update
        self.assertEqual(self.feature.edges[(0, 1, "MESSAGE")], 1)
        self.assertEqual(self.feature.edges[(0, 1, "LIKE")], 1)

    def test_update_neighbor(self):
        self.feature.neighbors[0] = [1, 2]

        # try to add an existing neighbor
        self.feature.update_neighbor(0, 1)
        self.assertEqual(self.feature.neighbors[0], [1, 2])

        # add a new neighbor
        self.feature.update_neighbor(0, 3)
        self.assertEqual(self.feature.neighbors[0], [1, 2, 3])

    def test_register_node(self):
        self.assertEqual(self.feature.register_node("A", 3), 4)
        self.assertEqual(self.feature.ids["A"], 3)
        self.assertEqual(self.feature.inv_ids[3], "A")
