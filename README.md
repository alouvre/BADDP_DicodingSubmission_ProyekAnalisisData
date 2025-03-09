# BADDP_DicodingSubmission_ProyekAnalisisData


## Description

This project is a part of the bike-sharing data analysis initiative, focusing on examining the Bike Sharing Dataset. The analysis results are then transformed into interactive data visualizations within a dashboard.

## Directory

- `/dashboard`: contains the file `func.py` which stores the functions needed by the dashboard
- `/data`: stores data used in the data analysis project
- `/image`: stores image and video assets used in this project
- `README.md`: file that provides information about this GitHub project
- `notebook.ipynb`: interactive jupyter notebook files to analyze data
- `requirements.txt`: file that stores information about the libraries used in this project
- `url.txt`: File containing links to the dashboard.
<!-- - `app.py`: main file to run the dashboard -->

## Installation

The steps to create your virtual environment from this project is as follows:

1. Clone this Repository
   ```bash
   git clone https://bikeshare-dashboard-dicoding-submission.streamlit.app/
   ```

2. Create Python Virtual Environment
   ```bash
   virtualenv venv
   ```

2. Activate the Environment
   ```bash
   venv\Scripts\activate
   ```

4. Install All the Requirements Inside "requirements.txt"
   ```bash
   pip install -r requirements.txt
   ```

5. Run the Streamlit Dashboard
   ```bash
   streamlit run dashboard/dashboard.py
   ```

6. Stop the application program by `ctrl + c`.