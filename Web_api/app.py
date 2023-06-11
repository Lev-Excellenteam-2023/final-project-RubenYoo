from flask import Flask, request

app = Flask(__name__)


@app.route('/', methods=['GET'])
def get_home_page():
    return 'Hello world'


@app.route('/', methods=['POST'])
def upload_file():

    file = request.files['file']  # Access the uploaded file
    print(file)

    return 'File uploaded successfully!'


if __name__ == '__main__':
    app.run()
