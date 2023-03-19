FROM pytorch/pytorch:1.11.0-cuda11.3-cudnn8-runtime

WORKDIR /

ARG AWS_ACCESS_KEY_ID
ARG AWS_DEFAULT_REGION
ARG AWS_SECRET_ACCESS_KEY
ARG BUCKET_NAME

ENV AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
ENV AWS_DEFAULT_REGION=${AWS_DEFAULT_REGION}
ENV AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
ENV BUCKET_NAME=${BUCKET_NAME}


# Install git
RUN apt-get update && apt-get install -y git

# Install python packages
RUN pip3 install --upgrade pip
ADD requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# We add the banana boilerplate here
ADD server.py .

# Add your model weight files 
# (in this case we have a python script)

ADD download.py .
RUN python3 download.py


# Add your custom app code, init() and inference()
ADD app.py .

EXPOSE 8000

CMD python3 -u server.py