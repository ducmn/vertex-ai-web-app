import os
from flask import json as fjson
from flask import Flask, render_template, request, redirect, url_for, json
from typing import Dict, List, Union

from google.cloud import aiplatform
from google.protobuf import json_format
from google.protobuf.struct_pb2 import Value

def predict_custom_trained_model_sample(
    project: str,
    endpoint_id: str,
    instances: Union[Dict, List[Dict]],
    location: str = "us-central1",
    api_endpoint: str = "us-central1-aiplatform.googleapis.com",
):
    """
    `instances` can be either single instance of type dict or a list
    of instances.
    """
    # The AI Platform services require regional API endpoints.
    client_options = {"api_endpoint": api_endpoint}
    # Initialize client that will be used to create and send requests.
    # This client only needs to be created once, and can be reused for multiple requests.
    client = aiplatform.gapic.PredictionServiceClient(client_options=client_options)
    # The format of each instance should conform to the deployed model's prediction input schema.
    instances = instances if type(instances) == list else [instances]
    instances = [
        json_format.ParseDict(instance_dict, Value()) for instance_dict in instances
    ]
    parameters_dict = {}
    parameters = json_format.ParseDict(parameters_dict, Value())
    endpoint = client.endpoint_path(
        project=project, location=location, endpoint=endpoint_id
    )
    response = client.predict(
        endpoint=endpoint, instances=instances, parameters=parameters
    )
    print("response")
    print(" deployed_model_id:", response.deployed_model_id)
    # The predictions are a google.protobuf.Value representation of the model's predictions.
    predictions = response.predictions
    finalresult = []
    for prediction in predictions:
        print(" prediction:", prediction)
        finalresult.append(prediction[0])
    return finalresult

app = Flask(__name__)
app.config['UPLOAD_PATH'] = 'static'

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/', methods = ['POST'])
def upload_file():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        myfile = fjson.loads(uploaded_file.read())
        result = predict_custom_trained_model_sample(
            project="195911317646",
            endpoint_id="6803496477701177344",
            location="europe-west2",
            instances=myfile,
            api_endpoint = "europe-west2-aiplatform.googleapis.com"
            )
    result = result[0]
    if result >= 0:
        result = ""
    else:
        result = "not "
    return render_template("result.html", result=result)