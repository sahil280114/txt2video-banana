from modelscope.pipelines import pipeline
from modelscope.outputs import OutputKeys
import boto3
import os

s3 = boto3.resource("s3")

BUCKET_NAME = os.getenv("BUCKET_NAME")

def upload_to_s3(path):
    s3.meta.client.upload_file(Bucket=BUCKET_NAME,Filename=path,Key=path.split("/")[-1])
    s3_url = f's3://{BUCKET_NAME}/{path.split("/")[-1]}'
    return s3_url

def init():
    global model
    model = pipeline('text-to-video-synthesis', 'damo/text-to-video-synthesis')

# Inference is ran for every server call
# Reference your preloaded global model variable here.
def inference(model_inputs:dict) -> dict:
    global model

    # Parse out your arguments
    prompt = model_inputs.get('prompt', None)
    if prompt == None:
        return {'message': "No prompt provided"}
    
    # Run the model
    input_prompt = {
        'text': prompt,
    }
    video_path = model(input_prompt,)[OutputKeys.OUTPUT_VIDEO]
    
    s3_path = upload_to_s3(video_path)

    # Return the results as a dictionary
    return {'video_url': s3_path}