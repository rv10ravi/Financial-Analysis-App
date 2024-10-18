import os
import json
from flask import Flask, request, render_template
from model import financial_analysis

app = Flask(__name__)

# Set upload folder
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def upload_file():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def handle_file_upload():
    if 'file' not in request.files:
        return 'No file part', 400
    
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        # Load the uploaded JSON file
        with open(filepath, 'r') as f:
            data = json.load(f)

        # Check if 'data' key exists and contains 'financials'
        if "data" not in data or "financials" not in data["data"]:
            return 'Invalid data structure', 400  # Return an error message if structure is wrong

        # Run financial analysis
        result = financial_analysis(data)
        
        # Render result in HTML template
        return render_template('results.html', result=json.dumps(result, indent=4))

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
