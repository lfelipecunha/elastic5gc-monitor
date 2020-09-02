from flask import Flask, request, jsonify
from pymongo import MongoClient
import datetime
import os

app = Flask(__name__)

client = MongoClient('mongodb://mongodb')
db = client.monitoring

@app.route('/entry/<int:amf_id>', methods=['POST'])
def new_entry(amf_id):
    data = request.form
    cpu_usage = data['cpu_usage']
    entry = {
        'amf_id': amf_id,
        'cpu_usage': cpu_usage,
        'created_at': datetime.datetime.now()
    }
    db.entries.insert_one(entry)
    return 'Ok'

@app.route('/entries/<int:num_of_periods>', methods=['GET'])
def get_entries(num_of_periods):
    period = int(os.environ['VERIFICATION_PERIOD'])
    seconds = period * num_of_periods
    start_date = datetime.datetime.now() - datetime.timedelta(seconds=seconds)

    data = db.entries.find({
        'created_at': {
            '$gte': start_date
        }
    })

    result = []
    for entry in data:
        cur_period = int((entry['created_at'] - start_date).total_seconds() / period)
        result.append({'amf_id': entry['amf_id'], 'cpu_usage': entry['cpu_usage'], 'period': cur_period})

    return jsonify(result)

app.run(host='0.0.0.0', debug=True)

