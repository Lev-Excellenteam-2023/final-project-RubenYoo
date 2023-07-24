from flask import Flask, request, make_response, jsonify
import uuid
import time
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

    engine = create_engine(f'sqlite:///../Database/db/mydatabase.db', echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()

    if email:
        user = session.query(User).filter_by(email=email).first()
        if user is None:
            user = User(email=email)
            session.add(user)
            session.commit()
            session.refresh(user)
    else:
        user = None

    upload = Upload(uid=str(uid), filename=file.filename,
                    upload_time=datetime.now(),
                    user=user)
    session.add(upload)
    session.commit()
    session.close()

    # Save the file
    file.save(f'uploads/{uid} {timestamp} {file.filename}')

    return {'uid': str(uid)}


@app.route('/<uid>', methods=['GET'])
def get_status_by_uid(uid):
    """
    Get status of a pptx file
    :param uid: the uid of the file
    :return: a json with the status of the file
    """

    # Fetch the upload from the DB
    engine = create_engine(f'sqlite:///../Database/db/mydatabase.db', echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    upload = session.query(Upload).filter_by(uid=uid).first()
    session.close()

    if not upload:
        return make_response(jsonify({'status': 'not found'}), 404)

    response_data = {
        "status": str(upload.status.value),
        "filename": str(upload.filename),
        "finish time": str(upload.finish_time)
    }

    return make_response(jsonify(response_data), 200)


@app.route('/<email>/<filename>', methods=['GET'])
def get_status_email_filename(email, filename):
    """
    Get status of a pptx file
    :param email: the uid of the file
    :param filename: the filename of the file
    :return: a json with the status of the file
    """

    # Fetch the upload from the DB
    engine = create_engine(f'sqlite:///../Database/db/mydatabase.db', echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    user = session.query(User).filter_by(email=email).first()
    upload = session.query(Upload).filter_by(user_id=user.id, filename=filename).first()
    session.close()

    if not upload:
        return make_response(jsonify({'status': 'not found'}), 404)

    response_data = {
        "status": str(upload.status.value),
        "filename": str(upload.filename),
        "finish time": str(upload.finish_time)
    }

    return make_response(jsonify(response_data), 200)


if __name__ == '__main__':
    app.run(debug=True)
