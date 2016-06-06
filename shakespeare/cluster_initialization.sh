#/usr/bin/bash

# This is an init script to be run to create the cluster and complete the job.
# This file can be run directly after creating the project or commands can be
# run from this file piecemeal

# The user will have to create her own project as this is not possible to be
# scripted at the current moment.  The project should be named
# bill-shakespeare-hadooop or the cluster create command below should be
# changed

# We create the bucket and put the file there to be accessed by the cluster
gsutil mb gs://bill-shakespeare
gsutil cp will_play_text.csv gs://bill-shakespeare-bucket/

gcloud dataproc clusters create bill-shakespeare \
    --zone us-central1-a \
    --master-machine-type n1-standard-2 \
    --master-boot-disk-size 500 \
    --num-workers 2 \
    --worker-machine-type n1-standard-2 \
    --worker-boot-disk-size 500 \
    --project bill-shakespeare-hadoop \

gcloud dataproc jobs submit pyspark \
    --cluster bill-shakespeare \
    --py-files pyspark_csv.py pyspark_count_shakespeare.py
