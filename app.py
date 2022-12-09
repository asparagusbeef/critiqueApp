from os import environ
from flask import Flask, render_template, request, flash
import openai
from oauth2client.service_account import ServiceAccountCredentials
import gspread
from datetime import datetime as dt
import json

def create_keyfile_dict():
    variables_keys = {
        "type": environ.get('SHEET_TYPE'),
        "project_id": environ.get('SHEET_PROJECT_ID'),
        "private_key_id": environ.get('SHEET_PRIVATE_KEY_ID'),
        "private_key": environ.get('SHEET_PRIVATE_KEY'),
        "client_email": environ.get('SHEET_CLIENT_EMAIL'),
        "client_id": environ.get('SHEET_CLIENT_ID'),
        "auth_uri": environ.get('SHEET_AUTH_URL'),
        "token_uri": environ.get('SHEET_TOKEN_URL'),
        "auth_provider_x509_cert_url": environ.get('SHEET_AUTH_PROVIDER_X509_CERT_URL'),
        "client_x509_cert_url": environ.get('SHEET_CLIENT_X509_CERT_URL')
    }
    return variables_keys

scopes = [
'https://www.googleapis.com/auth/spreadsheets',
'https://www.googleapis.com/auth/drive'
]
credentials = ServiceAccountCredentials.from_json_keyfile_name(json.dumps(create_keyfile_dict()), scopes) #access the json key you downloaded earlier 
file = gspread.authorize(credentials) # authenticate the JSON key with gspread
sheet = file.open("critiqueData") #open sheet
sheet = sheet.sheet1 #replace sheet_name with the name that corresponds to yours, e.g, it can be sheet1
def appendInputToSheets(sheet,assignment_type,prompt,text,ai_prompt,ai_response,user_rating="NA"):
    nrows = len(sheet.col_values(1))
    ncols = len(sheet.row_values(1))
    for col_index in range(ncols):
        col_index += 1
        if col_index == 1:
            sheet.update_cell(nrows, col_index, nrows+1)
        elif col_index == 2:
            sheet.update_cell(nrows+1, col_index, str(dt.now()))
        elif col_index == 3:
            sheet.update_cell(nrows+1, col_index, assignment_type)
        elif col_index == 4:
            sheet.update_cell(nrows+1, col_index, prompt)
        elif col_index == 5:
            sheet.update_cell(nrows+1, col_index, text)
        elif col_index == 6:
            sheet.update_cell(nrows+1, col_index, ai_prompt)
        elif col_index == 7:
            sheet.update_cell(nrows+1, col_index, ai_response)
        elif col_index == 8:
            sheet.update_cell(nrows+1, col_index, user_rating)
        else:
            print("out of bounds!")

openai.api_key = environ['OPENAI_API_KEY']

app = Flask(__name__)
app.secret_key = environ['APP_SECRET_KEY']

@app.route("/critiqueBeta")
def index():
    flash("-")
    flash("-")
    flash("-")
    flash("-")
    return render_template("index.html")

@app.route("/userInput", methods=["POST","GET"])
def submit():
    if str(request.form['radio-group-1670480900795'])=="option-1":
        assignment_type = "Essay"
    else:
        assignment_type = "Paragraph"
    prompt = str(request.form['textarea-1670481047558'])
    text = str(request.form['textarea-1670481047559'])
    flash(assignment_type)
    flash(prompt)
    flash(text)
    davinci_prompt = f"The following {assignment_type.lower()} was written according to a prompt.\n"+\
        "Please grade it on a scale of 1-100, and give a constructive critique on it\n\n"+\
            f"Prompt: {prompt}\n\n{assignment_type}:\n{text}\n\n ------------------------\n\n"
    output = openai.Completion.create(engine = "text-davinci-002", prompt = davinci_prompt)
    output_text = output.choices[0].text
    flash(output_text)
    appendInputToSheets(sheet,assignment_type,prompt,text,davinci_prompt,output_text)
    return render_template("index.html")
