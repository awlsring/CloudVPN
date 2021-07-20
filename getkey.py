import os
import re
import time
import boto3
from discord import Color
from botocore.exceptions import ClientError
import serverboi_utils.embeds as embed_utils
import serverboi_utils.responses as response_utils
from typing import List

BUCKET = os.environ.get("BUCKET")
REGION = os.environ.get("AWS_REGION")
WORKFLOW_NAME = "ProvisionVPN"
APPLICATION_ID = os.environ.get("APPLICATION_ID")
INTERACTION_TOKEN = os.environ.get("INTERACTION_TOKEN")
EXECUTION_NAME = os.environ.get("EXECUTION_NAME")

def main():
    config_path = '/wireguard/config'

    dirs = os.listdir(config_path)

    for dir in dirs:
        peers = []
        if 'peer' in dir:
            peers.append(dir)

    for peer in peers:
        peer_path = os.path.join(config_path, peer)

        peer_files = os.listdir(peer_path)

        file_urls = []

        for file in peer_files:
            if '.png' in file:
                s3 = boto3.client('s3')
                file_path = os.path.join(peer_path, file)

                try:
                    with open(file_path, "rb") as file:
                        object_name = f"/wireguard/{file}"
                        s3.upload_file(file_path, BUCKET, object_name)

                    file_urls.append(f"https://s3-{REGION}.amazonaws.com/{BUCKET}/{object_name}")
                except ClientError as error:
                    print(error)
                    fail_wf()
                    raise error

    update_workflow()
    post_qr_links()
    return True
    

def update_workflow(stage: str):
    print(stage)

    embed = embed_utils.form_workflow_embed(
        workflow_name=WORKFLOW_NAME,
        workflow_description=f"Workflow ID: {EXECUTION_NAME}",
        status="🟢 running",
        stage=stage,
        color=Color.green(),
    )

    data = response_utils.form_response_data(embeds=[embed])
    response_utils.edit_response(APPLICATION_ID, INTERACTION_TOKEN, data)

def post_qr_links(qr_urls: List[str]):
    content = ''
    i = 1
    for url in qr_urls:
        content = f'{content} QR Code {i}: {url}\n'

    data = response_utils.form_response_data(content=content)
    response_utils.post_new_response(APPLICATION_ID, INTERACTION_TOKEN, data)


def fail_wf(stage: str):
    embed = embed_utils.form_workflow_embed(
        workflow_name=WORKFLOW_NAME,
        workflow_description=f"Workflow ID: {EXECUTION_NAME}",
        status="❌ failed",
        stage=stage,
        color=Color.red(),
    )

    data = response_utils.form_response_data(embeds=[embed])
    response_utils.edit_response(APPLICATION_ID, INTERACTION_TOKEN, data)

if __name__ == 'main':
    main()