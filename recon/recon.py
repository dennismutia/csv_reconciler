import pandas as pd


def load_csv(path):
    '''
    Import CSV file
    '''
    return pd.read_csv(path, dtype={0: str})

class Reconciliation:
    def __init__(self, source_df, target_df):
        self.source_df = source_df
        self.target_df = target_df
        self.source_join_column = self.source_df.columns[0]
        self.target_join_column = self.target_df.columns[0]
    

    def get_records_not_in_target(self):
        '''
        Get records in source that are not in target
        '''
        missing_in_target = self.source_df[~self.source_df[self.source_join_column].isin(self.target_df[self.target_join_column])].dropna()
        missing_in_target_results = pd.DataFrame({
            "Type": "Missing in Target",
            "Record Identifier": missing_in_target[self.source_join_column]
        })
        return missing_in_target_results
    
    def get_records_not_in_source(self):
        '''
        Get records in target that are not in source
        '''
        missing_in_source = self.target_df[~self.target_df[self.target_join_column].isin(self.source_df[self.source_join_column])].dropna()
        missing_in_source_results = pd.DataFrame({
            "Type": "Missing in Source",
            "Record Identifier": missing_in_source[self.target_join_column]
        })
        return missing_in_source_results
    

    def get_all_columns(self):
        '''
        Get all columns from both files
        '''
        source_columns = self.source_df.columns[1:]
        target_columns = self.target_df.columns[1:]
        columns = set(source_columns.append(target_columns))
        return columns

    def compare_columns(self, columns):
        '''
        Compare columns between the two files
        '''
        
        results_df = pd.DataFrame()
        for column in columns:
            source_df = self.source_df[[self.source_join_column, column]].dropna()
            target_df = self.target_df[[self.target_join_column, column]].dropna()
            comparison_df = source_df.merge(target_df, how='inner', left_on=self.source_join_column, right_on=self.target_join_column, suffixes=('_source', '_target'))
            comparison_df = comparison_df[comparison_df[column + '_source'] != comparison_df[column + '_target']]
            differences_df = pd.DataFrame({
                "Type": "Field Discrepancy",
                "Record Identifier": comparison_df[self.source_join_column],
                "Field": column,
                "Source Value": comparison_df[column + '_source'],
                "Target Value": comparison_df[column + '_target']
            })
            results_df = pd.concat([results_df, differences_df])

        return results_df