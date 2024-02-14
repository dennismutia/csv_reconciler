import streamlit as st
import pandas as pd

from recon.recon import Reconciliation, load_csv

def main():
    st.title("CSV File Comparison App")

    # Upload CSV files
    st.sidebar.header("Upload CSV Files")
    source = st.sidebar.file_uploader("Upload source csv", type=["csv"])
    if source:
        source_df = load_csv(source)
        st.subheader("Data from source csv")
        st.write(source_df)

    target = st.sidebar.file_uploader("Upload target csv", type=["csv"])
    if target:
        target_df = load_csv(target)
        st.subheader("Data from target csv")
        st.write(target_df)

    if source is not None and target is not None:
        recon = Reconciliation(source_df, target_df)
        records_not_in_target = recon.get_records_not_in_target()
        records_not_in_source = recon.get_records_not_in_source()

        # compare columns
        st.sidebar.title("Column Selection")

        # Checkbox to select all columns
        select_all_columns = st.sidebar.checkbox("Select All Columns", key="select_all_columns")
        columns = recon.get_all_columns()
        if select_all_columns:
            selected_columns = columns
        else:
            selected_columns = st.sidebar.multiselect("Select columns for comparison", columns)
        column_comparison_df = recon.compare_columns(selected_columns)
        
        # Display results
        if column_comparison_df.empty:
            result_df = pd.concat([records_not_in_source, records_not_in_target])
        result_df = pd.concat([records_not_in_source, records_not_in_target, column_comparison_df])
        
        st.subheader("Reconciliation Results")
        if result_df.empty:
            st.success("No discrepancies found!")
        else:
            st.download_button(
                label="Download Reconciliation Results",
                data=result_df.to_csv(index=False),
                file_name="reconciliation_results.csv",
                mime="text/csv"
            )
            st.write(result_df)
    else:
        st.warning("Please upload both CSV files.")

if __name__ == "__main__":
    main()
