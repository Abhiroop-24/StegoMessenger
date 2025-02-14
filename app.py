from flask import Flask, render_template, request, send_file
from stego import hide_message, extract_message
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/hide', methods=['POST'])
def hide():
    image = request.files['image']
    message = request.form['message']
    password = request.form['password']
    image.save("temp.png")
    hide_message("temp.png", message, password, "hidden.png")
    return send_file("hidden.png", as_attachment=True)

@app.route('/extract', methods=['POST'])
def extract():
    image = request.files['image']
    password = request.form['password']
    image.save("uploaded.png")
    result = extract_message("uploaded.png", password)
    return f"Extracted Message: {result}"

if __name__ == '__main__':
    app.run(debug=True)