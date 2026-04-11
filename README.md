# Project Title: Car Finder

## Purpose
This project takes in data on several cars and returns the top 3 vehicles based on user preferences.
The user chooses what's important to them:
	- fuel efficiency
	- performance
	- "coolness"
The user's preferences are used as weights in a normalized scoring equation that determines the top 3.

## Dependencies
Libraries to install:
	- pandas (data handling, analysis)
	- python-dotenv (for environment variables)
	- install with: pip install pandas python-dotenv

Built-in modules:
	- json, smtplib, email, os

Required Files:
	- Automobile.csv (data)
	- input1.json-input7.json (test input)
	- .env (email credentials, not included)

External service:
	- Gmail SMTP

## How to run
python3 carFinder.py
The code will run through the test cases.

To enable the email service:
	- create a .env file with:
		EMAIL_ADDRESS=your_email@gmail.com
		EMAIL_PASSWORD=your_app_password
	- this is not your regular gmail password, but an app password (see source for more details).
	- add email recipient in email test files (input5.json-input7.json)

## Input format (JSON)

{
"eff_weight": 0.35,
"perf_weight": 0.1,
"c_weight": 0.55,
"return": "web"
}

Email inputs have return of "email" and also include recipient email:
	- "email": "USER_GMAIL@gmail.com"

## Author: William Fugate

## Acknowledgements/Sources
	- data: https://www.kaggle.com/datasets/tawfikelmetwally/automobile-dataset?resource=download
	- normalization: https://www.geeksforgeeks.org/data-analysis/normalization-and-scaling/
	- JSON handling: https://realpython.com/python-json/
	- pandas in Python: https://pandas.pydata.org/pandas-docs/stable/index.html
	- email setup and message code: https://hackr.io/blog/how-to-send-emails-with-python-using-gmail

AI Use
ChatGPT to brainstorm, for initial setup, to help with debugging, and as a spelling check.