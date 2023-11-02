# wind-energy-dashboard-streamlit
This repository is contains the project files that deal with the creation of a wind resource assessment dashboard using streamlit

Official Start of Version 1
- November 2, 2023

# Structure of a streamlit application
- .streamlit/
  - config.toml
- app.py
- requirements.txt
- setup.sh
- data/
  - dataset.csv
- modules/  
  - data_loader.py
  - helper_function.py
- pages/
  - overview.py
  - details.py
  - settings.py
- static/
  - images/
    - logo.png
  - stles/
    - custom.css
  - js/
    - script.js
- templates/
  - custom_template.html

## Explanation
- app.py is the main entry point of the streamlit app
- .streamlit/config.toml optional configuration file for setting up thigns like theme, page title, etc. 
- requirements.txt a list of python packages that are required for the app to run
- setup.sh an optional shell script that can be used to setup environment variables or streamlit setting when deploying
- data/ directory for storing data fiels such as csvs, excel files, or sqlite databases
- modules/ if the app has complex functionality, code can be organized into modules and import them in app.py
- pages/ for a multi-page app, each scrip represents a different page in the dashboard
- static/ holds static assets like images, css files for styling, and javascript files if necessary
- templates/ if you need custom HTML templates

### Additional
- wind-energy-streamlity/ (venv/)
- sql/ 




# Documentation of Creation
- Create a new repository in Github named "wind-energy-dashboard-streamlit" with a license and readme.md
- Create a .gitignore file that to disallow the uploading of **/.DS_Store
- Creation and activation of a virtual environment wind-energy-streamlit
  - Creation: `python3 -m venv wind-energy-streamlit`
  - Activation: `source wind-energy-streamlit/bin/activate `
  - Deactivation: `deactivate`
- Creation and use of a requirements.txt file which indicates all required packages for the project
