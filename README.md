# CrockPotSoup

## Description
A web application that analyzes text as input and produces tables, charts, and other visualizations
on word statistics.

## Requirements
### Python 3.6 
Other Python 3.x versions may work. I haven't tried them out

### virtualenv
The purpose of this is to isolate Python environments,
allowing you to install libraries without touching your base system install
of Python. This prevents conflicts with Python versions and other libraries
that may have compatibility issues. You just get what you need in your project

For more on this, check out the documentation here
https://docs.python.org/3.6/library/venv.html


### Dash
This is a Python framework for building analytical web applications without 
having to code JavaScript. It also eliminates the need for a third party analytics
API like Google Visualizations.

https://dash.plot.ly/installation


## Bootstrap 
Here's everything you need to configure your environment for development. Happy coding team :)

### Windows
Requires:
- python 3.6
- pip

1. Clone CrockPotSoup repository into a directory on your computer. (Mine is in Documents/GitHub)

    git clone <CrockPotSoup url>

2. Navigate to CrockPotSoup directory you just cloned

3. Create your virtual environment with the following command:

    py -3 -m virtualenv venv

4. Your virtual environment is now called "venv". Activate your virtual environment with the
following command:

    venv\Scripts\activate
     
    You will see now that your virtual environment has been activate as denoted by (venv). 
    You are now pulling from your install of Python within the venv folder.
    *Note: It is important to activate each time you make changes to ensure you have access to libraries that will be installed for this project. If you do not do this before running code, you may see errors indicating that you do not have libraries installed that are present in the Lib directory of your virtual environment Python install

5. Install Dash by running the following commands
    pip install dash==0.35.1  # The core dash backend
    pip install dash-html-components==0.13.4  # HTML components
    pip install dash-core-components==0.42.1  # Supercharged components
    pip install dash-table==3.1.11  # Interactive DataTable component (new!)


6. Install TextBlob library
    pip install -U textblob
    python -m textblob.download_corpora


### Mac
Requires:
- brew
- pip
- python 3.6

1. Clone CrockPotSoup repository into a directory on your computer. (Mine is in Documents/GitHub)

    git clone <CrockPotSoup url>

2. Navigate to CrockPotSoup directory you just cloned


3. Create your virtual environment with the following command:

    python3 -m virtualenv venv


4. Your virtual environment is now called "venv". Activate your virtual environment 
    
    . venv/bin/activate
    
    You will see now that your virtual environment has been activate as denoted by (venv). 
    You are now pulling from your install of Python within the venv folder.
    #####*Note: It is important to activate each time you make changes to ensure you have access to libraries that will be installed for this project. If you do not do this before running code, you may see errors indicating that you do not have libraries installed that are present in the Lib directory of your virtual environment Python install

    

5. Install Dash by running the following commands
    pip install dash==0.35.1  # The core dash backend
    pip install dash-html-components==0.13.4  # HTML components
    pip install dash-core-components==0.42.1  # Supercharged components
    pip install dash-table==3.1.11  # Interactive DataTable component (new!)


6. Install TextBlob library
    pip install -U textblob
    python -m textblob.download_corpora
    
    * I had a certificate issue on Mac. I'm not sure what you'll find on Windows. I ran the following
    commands to resolve it
    
    . /Applications/Python\ 3.6/Install\ Certificates.command 
    python -m textblob.download_corpora

     
