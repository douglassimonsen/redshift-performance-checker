import boto3
import shared

cloudformation = boto3.client("cloudformation")
s3 = boto3.resource("s3")


def delete_stack(stack: str) -> None:
    _, bucket, _ = shared.get_stack_resources(stack)
    for obj in s3.Bucket(bucket).objects.filter():
        s3.Object(bucket, obj.key).delete()
    cloudformation.delete_stack(StackName=stack)