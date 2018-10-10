from Quagga.Utils.ModelBuilder import ModelBuilder
from Quagga.Utils.BlockParser import BlockParser
from Quagga.Utils.EmailDirectoryReader import DirectoryReader, EmailDirectoryReader, TempQuaggaReader

from Quagga.Utils.EmailListReader import ListReaderRawEmailTexts, ListReaderExtractedBodies
from Quagga.Utils.Email import Email, serialize_quagga_email
from Quagga.Utils.EmailProcessor import EmailProcessor

import tensorflow as tf
from pprint import pprint
import json
import timeit

import os
import sys


def timemeasure(f):
    def wrapper(*args, **kwargs):
        start = timeit.default_timer()
        f(*args, **kwargs)
        stop = timeit.default_timer()
        print("total runtime: ", stop - start)

    return wrapper


class Quagga:
    INPUT_NAME = 'quagga.input'
    PREDICTED_NAME = 'quagga.predicted'
    PARSED_NAME = 'quagga.parsed'

    def __init__(self, email_reader, output_dir, model_builder=None, model=None,
                 block_parser=BlockParser()):
        if model_builder is None:
            model_builder = ModelBuilder()

        self.output_dir = output_dir

        # READ
        self.emails_input = email_reader

        # MODEL
        self.model_builder = model_builder
        self.model = model

        print("building model...")
        self.model_builder = model_builder
        if model is None:
            self.model_builder = model_builder
            self.model_builder.build()
            self.model = model_builder.quagga_model
            self.model.graph = tf.get_default_graph()
        else:
            self.model = model

        self.graph = tf.get_default_graph()
        print("done")

        # PREDICT

        # PARSE
        self.block_parser = block_parser

    @property
    def emails_body(self):
        return EmailProcessor(self, self.emails_input, self.output_dir, self.emails_input,
                              lambda email, _: email.clean_body, self.INPUT_NAME)

    @property
    def fileending_predicted(self):
        return '.' + self.PREDICTED_NAME + '.json'

    @property
    def fileending_parsed(self):
        return '.' + self.PARSED_NAME + '.json'

    @property
    def fileending_input(self):
        return '.' + self.INPUT_NAME + '.json'

    def _emails_processed(self, stage, input_reader, process_input, func):
        if input_reader is None:
            input_reader = process_input
        else:
            print("reading from .quagga files...")

        return EmailProcessor(self, self.emails_input, self.output_dir, input_reader, func, stage)

    def emails_predicted(self, input_reader=None):
        return self._emails_processed(self.PREDICTED_NAME, input_reader, self.emails_body,
                                      lambda email_body, _: self._predict(email_body))

    def emails_parsed(self, prediction_reader=None):
        return self._emails_processed(self.PARSED_NAME, prediction_reader, self.emails_predicted(),
                                      lambda email_prediction, email_input: self._parse(
                                          email_prediction, email_input))

    # @timemeasure
    # @profile
    def store_all(self, folder_name: str = None):
        if folder_name is None:
            folder_name = self.output_dir
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        print("store all")

        for count, email_input in enumerate(self.emails_input):
            self._log_progress(count, self.emails_input.length)
            self._store_all(folder_name, email_input)

        print("stored all stages in " + folder_name)

    # @profile
    def _store_all(self, folder_name, email_input):
        self._store_email(folder_name, email_input.filename_with_path, self.INPUT_NAME, email_input)
        predicted = self._predict(email_input.clean_body)
        self._store_email(folder_name, email_input.filename_with_path, self.PREDICTED_NAME, predicted)
        parsed = self._parse(predicted, email_input)
        self._store_email(folder_name, email_input.filename_with_path, self.PARSED_NAME, parsed)

    def store_input(self, folder_name: str = None):
        if folder_name is None:
            folder_name = self.output_dir
        self._store(folder_name, self.INPUT_NAME, self.emails_input)

    def store_predicted(self, folder_name: str = None):
        if folder_name is None:
            folder_name = self.output_dir
        self._store(folder_name, self.PREDICTED_NAME, self.emails_predicted())

    def store_parsed(self, folder_name: str = None, prediction_reader=None):
        if folder_name is None:
            folder_name = self.output_dir
        self._store(folder_name, self.PARSED_NAME, self.emails_parsed(prediction_reader))

    def _log_progress(self, count, total):
        if count % 10 == 0:
            sys.stdout.write('\r')
            sys.stdout.write(str(count) + " / " + str(total) + " ")

    @timemeasure
    def _store(self, folder_name, stage, emails):
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        print("storing " + stage)

        for count, (email_input, email) in enumerate(zip(self.emails_input, emails)):
            self._log_progress(count, self.emails_input.length)
            self._store_email(folder_name, email_input.filename_with_path, stage, email)

        print("stored " + stage + " in " + folder_name)

    def _store_email(self, folder_name, filename, stage, email):
        path = os.path.abspath(folder_name)
        filename = path + '/' + filename + '.' + stage + '.json'
        with open(filename, 'w+') as fp:
            json.dump({stage: email}, fp, default=serialize_quagga_email)

    def _build_model(self, model_builder=ModelBuilder(), model=None):
        with self.graph.as_default():
            print("building model...")
            self.model_builder = model_builder
            if model is None:
                self.model_builder = model_builder
                self.model_builder.build()
                self.model = model_builder.quagga_model
            else:
                self.model = model

    def _predict(self, mail_text):
        with self.graph.as_default():
            text_raw = mail_text
            text_lines = text_raw.split('\n')

            return self._prettify_prediction(*self.model.predict(text_lines))

    def _parse(self, email_prediction, email_input):
        return self.block_parser.parse_predictions(email_prediction, email_input)

    def _prettify_prediction(self, y, text_lines, label_encoder):
        labels = label_encoder.classes_
        predictions = []
        for yi, line in zip(y, text_lines):
            line_prediction = {
                'text': line,
                'predictions': {}
            }
            for li, label in enumerate(labels):
                line_prediction['predictions'][label] = yi[li]
            predictions.append(line_prediction)
        return predictions

    """def print_predictions(self):
        for email_predicted in self.emails_predicted():
            for line_prediction in email_predicted:
                print(str(line_prediction['predictions']) + ' ' + line_prediction['text'])"""


if __name__ == '__main__':
    input_dir = "../Tests/testData/enron_tiny"
    output_dir = "../Tests/testData/output"

    quagga = Quagga(EmailDirectoryReader(input_dir), output_dir)

    """print("========================= input ")
    for input in quagga.emails_input:
        pprint(input)

    print("========================= bodies ")
    for body in quagga.emails_body:
        pprint(body)

    print("========================= predictions ")
    for prediction in quagga.emails_predicted(
            input_reader=TempQuaggaReader('quagga.input', output_dir, output_func=lambda input: input['clean_body'])):
        pprint(prediction)

    print("========================= parsed ")
    for parsed in quagga.emails_parsed(prediction_reader=TempQuaggaReader('quagga.predicted', output_dir)):
        pprint(parsed)"""

    quagga.store_all(output_dir)
