Project Name: Python Finbot

Description:

This code is a simple Flask web application that evaluates a user’s financial health based on various inputs related to their income, savings, investments, loans, and expenditure. Here’s a breakdown of its functionality:

Features:

A.	Web Form (POST/GET):
The user is presented with a form (form.html) where they enter financial data such as monthly income, savings percentage, emergency fund status, investments, expected return, loan details, and monthly variance in expenditure.

B.	Form Data Processing:
Upon form submission (POST request), the code processes the input data and calculates key financial metrics like:
1.	Monthly savings
2.	Monthly expenditure
3.	Loan-to-income ratio
4.	Loan-to-savings ratio
5.	Expenditure variance percentage

C.	Financial Health Scoring:
A score (out of 10) is calculated to assess the user’s financial health, with deductions
based on various factors:
Criteria	Score
No emergency fund	-2
No investments	-1.5
High loan burden (e.g. loan-to-income ratio is above 40%)	-1 to -2
Expenditure variance exceeding 20%	-1.5
Insufficient savings percentage (less than 20%)	-1

D.	Result Display:
The final score and metrics are displayed on a results page (result-nochart.html),
along with key financial details like monthly savings, loan-to-income ratio, and
variance percentage.

Structure:
1.	/(Main route): Handles the user input via form.html, processes the financial data, and shows results on result_wo_chart.html.
2.	/login: A secondary route to showcase a basic conditional check with a dictionary, although this route doesn’t seem to be related to the main financial health calculation.

Key Flask Concepts Used:
1.	Routing: Defines paths for different views.
2.	Form Handling: Uses POST and GET methods to manage form submission and data processing.
3.	Template Rendering: Utilizes Jinja2 templates to display dynamic HTML pages based on server-side calculations.
How to Use?
Prerequisites:
Python3: 
Ensure you have Python installed on your system. 
You can download it from https://www.python.org/ 

PIP: 
pip is the package installer for Python. It allows you to install and manage additional libraries and dependencies that are not included in the standard Python library. With pip, you can easily install packages from the Python Package Index (PyPI) and other repositories.

Installing pip:

Refer: https://pip.pypa.io/en/stable/installation/
 
Flask: 
Flask is a lightweight web framework for Python. It is designed to make getting started quick and easy, with the ability to scale up to complex applications. Flask is known for its simplicity, flexibility, and fine-grained control.

Key Features:
-	Lightweight: Minimalistic core with optional extensions.
-	Modular: Use only the components you need.
-	Flexible: Provides the tools to build web applications without imposing a specific structure.
-	Built-in Development Server: Comes with a built-in server for development and debugging.
-	Jinja2 Templating: Uses Jinja2 for templating, allowing you to generate HTML dynamically.

Install Flask using pip if you haven't already using the following command in you terminal: pip install Flask

Installing requirements:
pip install -r requirements-dev.txt

Running the Program:
After successfully installing the project, and opening the project in your terminal run the following commands in your terminal or command prompt:
Steps to Run the Application
1.	Navigate to the Directory: Open a terminal and navigate to the directory containing the financial_health.py file.
cd path/to/your/directory
2.	Run the Flask Application: Execute the following command to start the Flask server:
python financial_health.py

Alternatively, you can open the file in python IDLE or any code editor and run the program from there.
Upon launching the program, you will be given a link in your shell/terminal, this is the link where the local webpage is hosted on your machine.

Access the Application: Open a web browser and go to http://127.0.0.1:5000/ (The website is usually hosted on this link, if not use the link in the output of the program), then you should see the Financial Health Assessment form.

Fill Out the Form: Enter your financial information in the form fields and submit the form.

View Results: After submitting the form, you will be redirected to a results page displaying your financial health score and detailed analysis.
