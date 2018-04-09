#/bin/sh
docker build -t predict-service .
docker tag predict-service gcr.io/imagerecognitionprototype/predict-service
gcloud docker -- push gcr.io/imagerecognitionprototype/predict-service
