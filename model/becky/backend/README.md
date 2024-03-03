# Store Choicy
This resp is for collecting all required data from different open data sources


## First Time Setup (for Web app only)
prepare python environment recommend(3.9+)

1. (Backend) Setup python virtual environment

under project root path
```
python -m venv venv

windows:   
venv\Scripts\activate.bat

Linux:
source venv/bin/activate

```

2. (Backend) Install required python packages
```
pip install -r requirements.txt
```
Also add python package to the requirement list after adding new module by
``` 
pip freeze > requirements.txt
```

3. (Backend) Run Flask
```
flask run
```

4. (Frontend) Install Nodejs if not yet installed from https://nodejs.org/en/

5. (Frontend) Go to /frontend and install required frontend modules
```
npm install
```

6. (Frontend) Run React
```
npm start
```
You can also refer to readme under /frontend/## First Time Setup

