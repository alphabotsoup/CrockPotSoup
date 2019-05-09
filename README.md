# CrockPotSoup

A web application that analyzes text as input and produces tables, charts, and other visualizations
on word statistics.

## Requirements
### Python 3.6 


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

1. Install Python
https://www.python.org/downloads/release/python-364/

    - Click on the version that matches your needs. For Windows make sure you select the right version
	
    - Follow the installation instructions

2. Open command line to verify your Python installation

3. Install pip 

    - Download pip from the link below
    
        https://bootstrap.pypa.io/get-pip.py
        
    - Open command prompt and navigate to the folder containing your get-pip.py script
    
    - Run the following command:
        
        python get-pip.py
        
    - Verify it was installed using the following command
    
        pip -V
        
4. Clone CrockPotSoup repository into a directory on your computer. (Mine is in Documents/GitHub)

    git clone https://github.com/alphabotsoup/CrockPotSoup.git
    
    - Alternatively you can download a zip file on your computer by clicking the Clone or download button and selecting
    the Download zip file option
    - Double click to unzip your file and follow the remaining steps below

5. Navigate to CrockPotSoup directory you just cloned

6. Install virtualenv

        sudo pip install virtualenv
        
7. Create your virtual environment with the following command:

    py -3 -m virtualenv venv

8. Your virtual environment is now called "venv". Activate your virtual environment with the
following command:

    venv\Scripts\activate
     
    You will see now that your virtual environment has been activate as denoted by (venv). 
    You are now pulling from your install of Python within the venv folder.
    *Note: It is important to activate each time you make changes to ensure you have access to libraries that will be     installed for this project. If you do not do this before running code, you may see errors indicating that you do not have libraries installed that are present in the Lib directory of your virtual environment Python install

9. Install requirements by running the following command:
        
        pip install requirements.txt

### Mac
Requires:
- brew
- pip
- python 3.6

1. Install Python
https://www.python.org/downloads/release/python-364/

    - Click on the version that matches your needs. For Mac, click Mac OS X
	
    - Follow the installation instructions

2. Open your terminal to verify your Python installation

        Shainas-Air:~ python --version
        Python 3.6.4

3. Install pip 

        sudo easy_install pip

4. Clone CrockPotSoup repository into a directory on your computer. (Mine is in Documents/GitHub)

    git clone https://github.com/alphabotsoup/CrockPotSoup.git
    
    - Alternatively you can download a zip file on your computer by clicking the Clone or download button and selecting
    the Download zip file option
    - Double click to unzip your file and follow the remaining steps below

5. Navigate to CrockPotSoup directory you just cloned

6. Install virtualenv

        sudo pip install virtualenv

7. Create your virtual environment with the following command in the root folder of the CrockPotSoup directory:

        python3 -m virtualenv venv


8. Your virtual environment is now called "venv". Activate your virtual environment 
    
        . venv/bin/activate
    
    You will see now that your virtual environment has been activate as denoted by (venv). 
    You are now pulling from your install of Python within the venv folder.
    *Note: It is important to activate each time you make changes to ensure you have access to libraries that will be installed for this project. If you do not do this before running code, you may see errors indicating that you do not have libraries installed that are present in the Lib directory of your virtual environment Python install

    

9. Install requirements by running the following command:
        
        pip install requirements.txt


     
