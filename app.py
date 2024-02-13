import streamlit as st
import pandas as pd

def main():
    st.title("CSV File Comparison App")

    # Upload CSV files
    st.sidebar.header("Upload CSV Files")
    source = st.sidebar.file_uploader("Upload source csv", type=["csv"])
    target = st.sidebar.file_uploader("Upload target csv", type=["csv"])

    if source is not None and target is not None:
        # Read CSV files
        source_df = pd.read_csv(source)
        target_df = pd.read_csv(target)

        # Display uploaded data
        st.subheader("Data from source csv")
        st.write(source_df)

        st.subheader("Data from target csv")
        st.write(target_df)

        # Compare files and identify missing records
        column_to_compare = source_df.columns[0]
        missing_in_target = source_df[~source_df[column_to_compare].isin(target_df[column_to_compare])].dropna()
        missing_in_source = target_df[~target_df[column_to_compare].isin(source_df[column_to_compare])].dropna()

        st.subheader("Records in Source Missing in Target")
        st.write(missing_in_target)

        st.subheader("Records in Target Missing in Source")
        st.write(missing_in_source)

    else:
        st.warning("Please upload both CSV files.")

if __name__ == "__main__":
    main()
