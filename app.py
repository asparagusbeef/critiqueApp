from os import environ
from flask import Flask, render_template, request, flash
import openai

openai.api_key = environ['OPENAI_API_KEY']

app = Flask(__name__)
app.secret_key = "***REMOVED***"

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
    return render_template("index.html")
