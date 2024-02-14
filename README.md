# CSV Reconciler
This is an application that read in two CSV files, reconciles the records, and produce a report detailing the differences between the two.

It can be used through the cli or through a user interface build using [streamlit](https://streamlit.io/)

## Requirements
The following are the app requirements:
- Python 3.12
- Docker (optional)

## Running the app
1. Create a new virtual environment
    `python -m venv reconciler_app`
2. Activate the venv
    `source reconciler_app\bin\activate`
3. Install required packages
    `pip install -r requirements.txt`

### Running app in cli
Run the following to run a reconciliation
`python csv_reconciler.py -s source_csv_path -t target_csv_path -o reconciliation_ouput_path

### Running app via Streamlit GUI
Run the command below inside the app root folder and follow the prompts on the screen
`streamlit run app.py --server.address=0.0.0.0`
