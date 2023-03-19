# In this file, we define download_model
# It runs during container build time to get model weights built into the container

from modelscope.pipelines import pipeline
from modelscope.outputs import OutputKeys
import os

def download_model():
    model = pipeline('text-to-video-synthesis', 'damo/text-to-video-synthesis',device="cpu")

if __name__ == "__main__":
    download_model()
    