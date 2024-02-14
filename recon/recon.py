import logging
import pandas as pd


def load_csv(path) -> pd.DataFrame:
    '''
    Import CSV file
    Parameters:
        path (str): path to the CSV file

    Returns:
        pd.DataFrame: dataframe from the CSV file
    '''
    try:
        logging.info(f"Loading file from {path}...")
        return pd.read_csv(path, dtype={0: str})
    except FileNotFoundError:
        logging.error(f"File not found at {path}. Please check the path and try again.")
    except pd.errors.ParserError as e:
        logging.error(f"Error parsing csv file. Details: {e}")
    except pd.errors.EmptyDataError as e:
        logging.error(f"Empty csv file.")
    except Exception as e:
        logging.error(f"An unexpected error occurred. Details: {e}")

    

class Reconciliation:
    def __init__(self, source_df, target_df) -> None:
        self.source_df = source_df
        self.target_df = target_df
        self.source_join_column = self.source_df.columns[0]
        self.target_join_column = self.target_df.columns[0]
    

    def get_records_not_in_target(self) -> pd.DataFrame:
        '''
        Get records in source that are not in target
        Returns:
            pd.DataFrame: records not in target
        '''
        logging.info("Getting records missing in target...")
        missing_in_target = self.source_df[~self.source_df[self.source_join_column].isin(self.target_df[self.target_join_column])].dropna()
        missing_in_target_results = pd.DataFrame({
            "Type": "Missing in Target",
            "Record Identifier": missing_in_target[self.source_join_column]
        })
        logging.info("Done!")
        return missing_in_target_results
    
    def get_records_not_in_source(self) -> pd.DataFrame:
        '''
        Get records in target that are not in source

        Returns:
            pd.DataFrame: records not in source
        '''
        logging.info("Getting records missing in source...")
        missing_in_source = self.target_df[~self.target_df[self.target_join_column].isin(self.source_df[self.source_join_column])].dropna()
        missing_in_source_results = pd.DataFrame({
            "Type": "Missing in Source",
            "Record Identifier": missing_in_source[self.target_join_column]
        })
        logging.info("Done!")
        return missing_in_source_results
    

    def get_all_columns(self) -> set:
        '''
        Get all columns from both files

        Returns:
            columnsset: unique columns from both files

        '''
        source_columns = self.source_df.columns[1:]
        target_columns = self.target_df.columns[1:]
        columns = set(source_columns.append(target_columns))
        return columns

    def compare_columns(self, columns) -> pd.DataFrame:
        '''
        Compare columns between the two files

        Parameters:
            columns (list): list of columns to compare
        
        Returns:
            pd.DataFrame: dataframe of discrepancies
        '''

        logging.info("Comparing source and target columns...")
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
        logging.info("Done!")

        return results_df