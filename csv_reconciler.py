import argparse
import logging
import pandas as pd

from recon.recon import load_csv, Reconciliation  # assuming recon.py is in the same directory

logging.basicConfig(level=logging.INFO, format='%(message)s')

def parse_arguments():
    parser = argparse.ArgumentParser(description='CLI for reconciliation')
    parser.add_argument('--source', '-s', type=str, required=True, help='Path to the source CSV file')
    parser.add_argument('--target', '-t', type=str, required=True, help='Path to the target CSV file')
    parser.add_argument('--output', '-o', type=str, help='Path to the output CSV file')
    return parser.parse_args()

def main():
    args = parse_arguments()
    source_df = load_csv(args.source)
    target_df = load_csv(args.target)
    recon = Reconciliation(source_df, target_df)
    
    logging.info("-----> Starting reconciliation...")
    records_not_in_target = recon.get_records_not_in_target()
    records_not_in_source = recon.get_records_not_in_source()
    
    all_columns = recon.get_all_columns() 
    column_differences = recon.compare_columns(all_columns)

    logging.info("Reconciliation completed:")
    logging.info(f"- Records not in target: {records_not_in_target.shape[0]}")
    logging.info(f"- Records not in source: {records_not_in_source.shape[0]}")
    logging.info(f"- Records with field discrepancies: {column_differences.shape[0]}")

    result_df = pd.concat([records_not_in_source, records_not_in_target, column_differences])
    if args.output:
        result_df.to_csv(args.output, index=False)
        logging.info(f"\nResults saved to: {args.output}")


if __name__ == '__main__':
    main()