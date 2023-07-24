from flask import Flask, request, make_response
import uuid
import time
import os
import json
import glob
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Database.database_orm import Upload, User
from datetime import datetime

app = Flask(__name__)


@app.route('/', methods=['POST'])
def upload_file():
    """
    Upload a file to the server
    :return: a json with the uid of the file
    """

    # Access the uploaded file
    file = request.files['file']
    timestamp = time.time()

    secret_string = file.filename + str(timestamp)
    namespace = uuid.uuid4()

    # Generate a random UUID as the namespace
    uid = uuid.uuid5(namespace, secret_string)

    # Access optional email parameter
    email = request.form.get('email')

    # Create an Upload object and commit it to the database
    db_path = os.path.join(os.path.dirname(__file__), '../Database/db/mydatabase.db')
    engine = create_engine(f'sqlite:///{db_path}', echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    upload = Upload(uid=str(uid), filename=file.filename,
                    upload_time=datetime.now(),
                    user=None if email is None else session.query(User).filter_by(email=email).first())
    session.add(upload)
    session.commit()
    session.close()

    # Save the file
    file.save(f'uploads/{uid} {timestamp} {file.filename}')

    return {'uid': str(uid)}


@app.route('/<uid>', methods=['GET'])
def get_pptx_parsed(uid):
    """
    Get the parsed file
    :param uid: the uid of the file
    :return: a json with the status of the file
    """

    uploads_pattern = './uploads/*.pptx'
    outputs_pattern = './outputs/*.json'
    file_name = None
    timestamp = None
    explanation = None
    http_code = 404
    status = 'not found'

    for file_path in glob.glob(uploads_pattern):
        file_full_name = str(os.path.splitext(os.path.basename(file_path))[0])
        uid_file = file_full_name.split(' ')[0]
        print(uid_file)
        timestamp_file = file_full_name.split(' ')[1]
        print(timestamp_file)
        file_real_name = ' '.join(file_full_name.split(' ')[2:])
        print(file_real_name)

        if uid_file == uid:
            file_name = file_real_name
            timestamp = timestamp_file
            http_code = 200
            if uid not in [os.path.splitext(os.path.basename(file_path))[0].split(' ')[0] for file_path in
                           glob.glob(outputs_pattern)]:
                status = 'pending'
            else:
                status = 'done'
                with open(f'./outputs/{uid} {timestamp} {file_name}.json', 'r') as file:
                    explanation = json.load(file)

    response_data = {
        "status": status,
        "filename": file_name,
        "timestamp": timestamp,
        "explanation": explanation
    }

    response = make_response(response_data)
    response.status_code = http_code
    return response


if __name__ == '__main__':
    app.run(debug=True)
