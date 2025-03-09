# BADDP_DicodingSubmission_ProyekAnalisisData


## Description

This project is part of the bike sharing data analysis project to analyze the Bike Sharing Dataset. The results of the analysis are then made into the form of data visualization into an interactive dashboard.

## Directory

- `/image`: stores image and video assets used in this project
- `/dashboard`: contains the file `func.py` which stores the functions needed by the dashboard
- `/data`: stores data used in the data analysis project
- `README.md`: file that provides information about this GitHub project
<!-- - `app.py`: main file to run the dashboard -->
- `notebook.ipynb`: interactive jupyter notebook files to analyze data
- `requirements.txt`: file that stores information about the libraries used in this project

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