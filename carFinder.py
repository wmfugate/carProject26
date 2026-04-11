#Car Finder
#This projects takes in data from several cars (source listed at bottom)
#The user chooses what's important to them >> mpg/fuel efficiency, performance, "coolness"
#User's choice affects weights in scoring equation
#Program takes weights and uses them to rank the cars and return the "best" car for the user

import pandas as pd
import json
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

df = pd.read_csv("Automobile.csv")  #downloaded data
df = df.set_index("name")   #helps when taking name and finding corresponding data for return
#print(df.columns)

def test(fileName):
    with open(fileName) as file:   #test user preferences
        data = json.load(file)

    #JSON weights: efficieny_weight (on mpg), performance_weight (acceleration), and coolness_weight (horsepower + more?)
    #Final score = each weight * normalized value (since all different ranges, units >> now all 1 scale) summed
    #normalized value = (x - min)/(max - min)

    df["mpg_norm"] = (df["mpg"] - df["mpg"].min()) / (df["mpg"].max() - df["mpg"].min())
    df["acc_norm"] = 1 - (df["acceleration"] - df["acceleration"].min()) / (df["acceleration"].max() - df["acceleration"].min())
    df["hp_norm"] = (df["horsepower"] - df["horsepower"].min()) / (df["horsepower"].max() - df["horsepower"].min())

    df["score"] = df["mpg_norm"] * data["eff_weight"] + df["acc_norm"] * data["perf_weight"] + df["hp_norm"] * data["c_weight"]

    top3list = list(zip(df.sort_values(by="score", ascending=False).head(3).index, df.sort_values(by="score", ascending=False).head(3)["model_year"], df.sort_values(by="score", ascending=False).head(3)["score"]))   #sorts score values from greatest to least >> gets top 3 names, stored in list
    #print(top3list)

    if(top3list[0][2] == 0 and top3list[1][2] == 0 and top3list[2][2] == 0):
        print("No preference/weights inputted.")
        return

    if(data["return"] == "web"):
        #returns JSON format
        top = {"car name 1": top3list[0][0], "year 1": str(top3list[0][1]),
                "car name 2": top3list[1][0], "year 2": str((top3list[1][1])),
                "car name 3": top3list[2][0], "year 3": str((top3list[2][1]))}
        #year converted to string to allow json conv
        print(json.dumps(top))

        #if want to actually write json file to return:
        #with open("returnjson.json", "w") as retFile:
            #json.dump(top, retFile)
    elif(data["return"] == "email"):
        #returns via email
        load_dotenv()

        # Email Configuration -- grabs from file where stored
        SMTP_SERVER = "smtp.gmail.com"
        SMTP_PORT = 587
        EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
        EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
        
        body = "1st Best Car: " + top3list[0][0] + " " + str(top3list[0][1]) +"\n\n2nd Best Car: " + top3list[1][0] + " " + str(top3list[1][1]) + "\n\n3rd Best Car: " + top3list[2][0] + " " + str(top3list[2][1])

        try:
            msg = MIMEMultipart()
            msg['From'] = EMAIL_ADDRESS
            msg['To'] = data["email"]
            msg['Subject'] = "Best Cars for You"

            msg.attach(MIMEText(body, 'plain'))

            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()
                server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                server.sendmail(EMAIL_ADDRESS, data["email"], msg.as_string())
            
            print("Email sent successfully!")
        except Exception as e:
            print(f"Error sending email: {e}")
    else:
        print("That return path is not implemented.")
        #add error code?


print("Tests 1-4 return JSON formatted strings (as if returning back to user via web)\n"
"Tests 5-7 return an email to a test account\n"
"Test 7 is meant as a error check (no preferences entered)\n")
#this is a loop to go through the test JSONs
for i in range (1,8):
    print("\n\nTest #", i, ":", sep='')
    test("input" + str(i) + ".json")


#Sources:
#data from https://www.kaggle.com/datasets/tawfikelmetwally/automobile-dataset?resource=download
#normalization from https://www.geeksforgeeks.org/data-analysis/normalization-and-scaling/
#learning how to input/output JSON w/Python https://realpython.com/python-json/
#pandas for data in Python https://pandas.pydata.org/pandas-docs/stable/index.html
#email setup and message code https://hackr.io/blog/how-to-send-emails-with-python-using-gmail