import unittest
import pandas as pd
from recon.recon import Reconciliation

class TestReconciliation(unittest.TestCase):
    def setUp(self):
        self.source_df = pd.read_csv('data/source.csv', dtype={0: str})
        self.target_df = pd.read_csv('data/target.csv', dtype={0: str})

    def test_get_records_not_in_target(self):
        reconciliation = Reconciliation(self.source_df, self.target_df)
        result_df = reconciliation.get_records_not_in_target()
        self.assertEqual(result_df.shape[0], 1)

    def test_get_records_not_in_source(self):
        reconciliation = Reconciliation(self.source_df, self.target_df)
        result_df = reconciliation.get_records_not_in_source()
        self.assertEqual(result_df.shape[0], 1)

    def test_compare_columns(self):
        reconciliation = Reconciliation(self.source_df, self.target_df)
        all_columns = reconciliation.get_all_columns()
        result_df = reconciliation.compare_columns(all_columns)
        self.assertEqual(result_df.shape[0], 1)


if __name__ == '__main__':
    unittest.main()
