python -m venv myenv
.\myenv\Scripts\activate

.\myenv\Scripts\python.exe -m pip install ipykernel
.\myenv\Scripts\python.exe -m ipykernel install --user --name myenv --display-name "Python (myenv)"
.\myenv\Scripts\python.exe -m pip install pandas
.\myenv\Scripts\python.exe -m pip install openpyxl
.\myenv\Scripts\python.exe -m pip install seaborn
.\myenv\Scripts\python.exe -m pip install matplotlib
.\myenv\Scripts\python.exe -m pip install pyodbc 
.\myenv\Scripts\python.exe -m pip install sqlalchemy
.\myenv\Scripts\python.exe -m pip install scipy
.\myenv\Scripts\python.exe -m pip install scikit-learn
.\myenv\Scripts\python.exe -m pip install joblib
.\myenv\Scripts\python.exe -m pip install xgboost==2.0.3
