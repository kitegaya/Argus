import argparse, json, uuid, os, boto3
from datetime import datetime

TABLE_NAME  = os.environ.get('DYNAMODB_TABLE', 'argus-incidents')
BUCKET_NAME = os.environ.get('S3_BUCKET', 'argus-reports-default')

dynamodb = boto3.resource('dynamodb')
s3       = boto3.client('s3')

def store(postmortem: dict):
    incident_id = str(uuid.uuid4())
    postmortem['incident_id'] = incident_id
    postmortem['timestamp']   = datetime.utcnow().isoformat()

    table = dynamodb.Table(TABLE_NAME)
    table.put_item(Item=postmortem)
    print(f'Written to DynamoDB: {incident_id}')

    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=f'reports/{incident_id}.json',
        Body=json.dumps(postmortem, indent=2),
    )
    print(f'Written to S3: reports/{incident_id}.json')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--postmortem', required=True)
    args = parser.parse_args()

    with open(args.postmortem) as f:
        postmortem = json.load(f)

    store(postmortem)
