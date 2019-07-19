import json
from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

config_file = "./config.json"
config = dict()

with open(config_file) as jsn:
    obj = json.load(jsn)
    config = obj

"""
    Manage a configuration file.
    Exposes API to read/write the configuration file
    
    No Access control
"""

class TrackerContractGet(Resource):

    def get(self):

        return {'result': config["tracker"]["address"]}

# class TrackerContractPut(Resource):

    def put(self):

        config["tracker"]["address"] = request.form['data']
        # Write modification in local file
        with open(config_file, 'w') as outfile:
            json.dump(config, outfile, indent=4)

        return {'status': 200}


api.add_resource(TrackerContractGet, '/tracker')
#api.add_resource(TrackerContractPut, '/tracker')

if __name__ == '__main__':
    
    app.run(host="0.0.0.0", port=80, debug=True)