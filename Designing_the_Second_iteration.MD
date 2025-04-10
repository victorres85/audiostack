# Assignment

Your CTO has asked you to do a short design task
Building from your MVP, they want to know how you would approach the following
extensions in functionality:
1. Making the API asynchronous in its behaviour
2. Making the API able to handle larger files (up to 1hr in duration)
3. Creating a cache so the same files don’t get reprocessed each time they are
called.
The CTO wants you to
1. Pick one of these features that you think would be the most value to a
customer
2. Explain why this should be worked on
3. Create a simple design proposal for implementing it

## Feature most valueble for a customer

### My pick
Making the API asynchronous in its behaviour

### Why this should be worked on:
1. Improve user experience, users have the tendency not to wait long time for a request response, by making the api asynchronous we would be able to quickly aknowledge the user that we have received the request and are proccessing it.
2. Would create the foundation to build the second feature which would allow the users to handle larger files.

### Design proposal
Would suggest to have this application divided between the following layers:
API, Queue and Lambda:

The following AWS services would be used: SQS Queue, S3Bucket, Lambda Function, RDS.

#### Api endpoints:
POST /convert/{output_format}
*   accepts the audio file
*   sends message to sqs queue for processing
*   saves relevant information to db
*   saves uploaded file into S3Bucket
*   returns message confirming status: processing plus the task-id

GET /status/{task_id}
*   returns the status of the task and in case the status is complete return also the newly generated file

#### SQS Queue
Serving as mesage broker

#### AWS Lambda Fuction
responsable for converting the file, upload the converted file to S3Bucket and update the status of the task on the Database
