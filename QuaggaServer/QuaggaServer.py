from flask import Flask, request
from flask.json import jsonify


from Quagga import Quagga, ModelBuilder, ListReaderExtractedBodies



quagga = Quagga(ListReaderExtractedBodies(''), '')
model_cache = {
    5: {
        True: {
            'enron': None,
            'asf': None
        },
        False: {
            'enron': None,
            'asf': None
        }
    },
    2: {
        True: {
            'enron': None,
            'asf': None
        },
        False: {
            'enron': None,
            'asf': None
        }
    }
}

app = Flask(__name__)


@app.route('/index')
def root():
    return app.send_static_file('index.html')

def predict(lines, crf, trainset, text):
    try:
        print(model_cache)
        model = model_cache[lines][crf][trainset]
        if model is None:
            raise KeyError
        quagga._build_model(model=model)
    except KeyError:
        model_builder = ModelBuilder(with_crf=crf, zones=5, trainset=trainset)
        model = quagga._build_model(model_builder)
        model_cache[5][crf][trainset] = model


    return quagga._predict(text)

@app.route('/five', methods=['POST'])
def five():
    data = request.get_json()
    prediction = predict(5, data.get('model', '') == 'crf', data.get('trainedOn', 'enron'), data.get('rawText'))
    return jsonify(prediction)


@app.route('/two', methods=['POST'])
def two():
    data = request.get_json()
    prediction = predict(2, data.get('model', '') == 'crf', data.get('trainedOn', 'enron'), data.get('rawText'))
    return jsonify(prediction)


if __name__ == '__main__':
    # export FLASK_APP=QuaggaServer.py
    # flask run
    app.run()
