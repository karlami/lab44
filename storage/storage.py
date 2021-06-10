import os
import shutil
from datetime import datetime, timedelta

from azure.storage.blob import BlobServiceClient, generate_account_sas, ResourceTypes, AccountSasPermissions, \
    ContainerClient

ACCESS_KEY = "tQtWUdxCXuC9oYg4O3IEqwRyeHFCui/enNkQhrQGrXhYLv1deslS7C7n1fftwDrFEm3u7Qf8rK6oIe5fjul2fA=="


def get_sas(type):
    if type == 0:  # Only read
        sas_token = generate_account_sas(
            account_name="proyectosoa",
            account_key=ACCESS_KEY,
            resource_types=ResourceTypes(service=True, container=True, object=True),
            permission=AccountSasPermissions(read=True),
            expiry=datetime.utcnow() + timedelta(minutes=480)
        )
    elif type == 1:  # Only write
        sas_token = generate_account_sas(
            account_name="proyectosoa",
            account_key=ACCESS_KEY,
            resource_types=ResourceTypes(service=True, container=True, object=True),
            permission=AccountSasPermissions(write=True),
            expiry=datetime.utcnow() + timedelta(minutes=480)
        )
    else:  # Read, write and list
        sas_token = generate_account_sas(
            account_name="proyectosoa",
            account_key=ACCESS_KEY,
            resource_types=ResourceTypes(service=True, container=True, object=True),
            permission=AccountSasPermissions(write=True, read=True, list=True),
            expiry=datetime.utcnow() + timedelta(minutes=480)
        )
    return sas_token


def create_container(container_name):
    credential = get_sas(3)
    blob_service_client = BlobServiceClient(account_url="https://proyectosoa.blob.core.windows.net/",
                                            credential=credential)

    print(blob_service_client.url)

    container_client = blob_service_client.get_container_client(container_name)
    response = ""

    try:
        container_client.create_container()
        response = "Container " + container_name + " created successful"
    except:
        response = "Container " + container_name + " couldn't be created"

    return response


def upload_file(container_name, file):
    credential = get_sas(1)
    blob_service_client = BlobServiceClient(account_url="https://proyectosoa.blob.core.windows.net/",
                                            credential=credential)
    response = ""
    try:
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=file.filename)
        blob_client.upload_blob(file)
        response = "File uploaded successful"
    except:
        response = "Error uploading file"

    return response


def download(container_name, filename):
    credential = get_sas(2)
    blob_service_client = BlobServiceClient(account_url="https://proyectosoa.blob.core.windows.net/",
                                            credential=credential)
    container_client = blob_service_client.get_container_client(container_name)
    blobs = container_client.list_blobs()

    #_create_dirs("/storage_api/tempfile")

    for blob in blobs:
        if blob.name == filename:
            path_ = os.path.dirname(__file__) + "/tempfile/"
            fname = os.path.join(path_, blob.name)
            client = blob_service_client.get_blob_client(container_name, blob)
            with open(fname, "wb") as download_file:
                download_file.write(client.download_blob().readall())
            print("Downloading file to: " + fname)
    return "ok"


def _create_dirs(dest_path):
    if not os.path.exists(dest_path):
        os.makedirs(dest_path)
    elif not os.path.isdir(dest_path):
        shutil.rmtree(dest_path)
        os.makedirs(dest_path)


create_container("test1")