from flask import Flask, request, jsonify
from pymongo import MongoClient
import datetime
import os
import argparse
import yaml

app = Flask(__name__)

parser = argparse.ArgumentParser(description='Elastic Monitor')
parser.add_argument('--config', help="Configuration File")
args = parser.parse_args()
yml_file = open(os.path.abspath(os.path.join(os.path.abspath(__file__), '..', args.config)))
config = yaml.load(yml_file, Loader=yaml.CLoader)


client = MongoClient('mongodb://' + config.get('database_uri', ''))
db = client.monitoring
time_window = config.get('time_window', 2)

def generate_sequency(date):
    seconds = int(date.strftime('%S'))
    seq = int(seconds/time_window)
    return date.strftime('%y%m%d%H%M')+str(seq).rjust(2,'0')

@app.route('/entry/<int:amf_id>', methods=['POST'])
def new_entry(amf_id):

    data = request.form
    cpu_usage = data['cpu_usage']
    date = datetime.datetime.now()
    sequency = generate_sequency(date)
    app.logger.debug('Sequency: ' + sequency)
    entry = {
        'amf_id': amf_id,
        'cpu_usage': cpu_usage,
        'created_at': date,
        'sequency': sequency
    }
    db.entries.insert_one(entry)
    return 'Ok'

@app.route('/entries/<int:num_of_intervals>', methods=['GET'])
def get_entries(num_of_intervals):


    aggregations = [
        {
            '$group': {
                '_id': '$sequency',
                'count': {'$sum': 1},
                'entries': {'$push': {'cpu_usage':'$cpu_usage', 'created_at': '$created_at', 'amf_id': '$amf_id'}}
            }
        },
        {
            '$sort': {
                '_id': -1
            }
        },
        {
            '$limit': num_of_intervals
        }
    ]


    initial_sequency = request.args.get('initial_sequency', None)

    if initial_sequency != None:
        aggregations.insert(0, {'$match': {'sequency': { '$gte': initial_sequency}}})

    entries = db.entries.aggregate(aggregations)

    result = []
    for seq in entries:
        result.append(seq)

    return jsonify(result)

app.run(host='0.0.0.0', debug=True)

