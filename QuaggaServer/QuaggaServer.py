from flask import Flask, request
from flask.json import jsonify

from Quagga import Quagga, ModelBuilder, ListReaderExtractedBodies

quagga = Quagga(ListReaderExtractedBodies(''), '')
model_cache = {}

app = Flask(__name__)


@app.route('/index')
def root():
    return app.send_static_file('index.html')


def predict(data, n_zones):
    # get values from request data
    use_crf = data.get('model', '') == 'crf'
    train_set = data.get('trainedOn', 'enron')
    cache_key = '{}_{}_{}'.format(n_zones, use_crf, train_set)

    # add model to cache if it's missing
    if cache_key not in model_cache:
        model_builder = ModelBuilder(with_crf=use_crf, zones=n_zones, trainset=train_set)
        model = quagga.build_model_from(model_builder)
        model_cache[cache_key] = model

    # make Quagga use requested model
    else:
        quagga.set_model(model_cache[cache_key])

    # run Quagga on requested data
    text = data.get('rawText')
    return quagga.predict(text)


@app.route('/two', methods=['POST'])
def two():
    data = request.get_json()
    prediction = predict(data, n_zones=2)
    return jsonify(prediction)


@app.route('/five', methods=['POST'])
def five():
    data = request.get_json()
    prediction = predict(data, n_zones=5)
    return jsonify(prediction)


if __name__ == '__main__':
    # export FLASK_APP=QuaggaServer.py
    # flask run
    app.run()
