import boto3


cloudformation = boto3.client("cloudformation")


def get_stack_resources(stack: str) -> tuple[str, str, list[dict]]:
    resources = cloudformation.list_stack_resources(StackName=stack)[
        "StackResourceSummaries"
    ]
    redshift_id = bucket = None
    usernames = []
    for resource in resources:
        if resource["ResourceType"] == "AWS::Redshift::Cluster":
            redshift_id = resource["PhysicalResourceId"]
        elif resource["ResourceType"] == "AWS::S3::Bucket":
            bucket = resource["PhysicalResourceId"]
        elif resource["ResourceType"] == "AWS::IAM::User":
            usernames.append(resource["PhysicalResourceId"])

    if redshift_id is None or bucket is None or not usernames:
        raise ValueError
    return redshift_id, bucket, usernames