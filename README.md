# BADDP_DicodingSubmission_ProyekAnalisisData

## Directory

- `/assets`: stores image and video assets used in this project
- `/dashboard`: contains the file `func.py` which stores the functions needed by the dashboard
- `dataset`: stores data used in the data analysis project
- `README.md`: file that provides information about this GitHub project
- `app.py`: main file to run the dashboard
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
   streamlit run app.py
   ```

6. Stop the application program by `ctrl + c`.