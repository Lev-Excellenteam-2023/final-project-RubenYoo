from flask import Flask, request
import uuid
import time
import os
import json
import glob

app = Flask(__name__)


@app.route('/', methods=['POST'])
def upload_file():
    # Access the uploaded file
    file = request.files['file']
    timestamp = time.time()

    secret_string = file.filename + str(timestamp)
    namespace = uuid.uuid4()

    # Generate a random UUID as the namespace
    uid = uuid.uuid5(namespace, secret_string)

    # Save the file
    file.save(f'uploads/{uid} {timestamp} {file.filename}.pptx')

    return {'uid': str(uid)}


@app.route('/<uid>', methods=['GET'])
def get_pptx_parsed(uid):
    uploads_pattern = './uploads/*.pptx'
    outputs_pattern = './outputs/*.json'
    file_name = None
    timestamp = None
    explanation = None

    # uid not uploaded
    if uid not in [os.path.splitext(os.path.basename(file_path))[0] for file_path in glob.glob(uploads_pattern) if not
                   os.path.isdir(file_path)]:
        status = 'not found'

    # uid not processed
    elif uid not in [os.path.splitext(os.path.basename(file_path))[0] for file_path in glob.glob(outputs_pattern) if
                     not os.path.isdir(file_path)]:
        status = 'pending'

    # file is processed
    else:
        status = 'done'
        with open(f'./outputs/{uid}.json', 'r') as file:
            explanation = json.load(file)

    return {"status": status, "filename": file_name, "timestamp": timestamp, "explanation": explanation}


if __name__ == '__main__':
    app.run()
