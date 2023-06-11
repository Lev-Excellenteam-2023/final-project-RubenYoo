from flask import Flask, request
import uuid
import time

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
    file.save(f'uploads/[{uid}][{timestamp}][{file.filename}].pptx')

    return {'uid': str(uid)}


if __name__ == '__main__':
    app.run()
