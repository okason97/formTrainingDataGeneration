from __future__ import print_function

from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

def get_folder_id(service, name):
    try:
        response = service.files().list(q="mimeType = 'application/vnd.google-apps.folder' and name = '{}'".format(name),
                                        spaces='drive',
                                        fields='files(id, name)').execute()
        id = None
        for file in response.get('files', []):
            id = file.get("id")
    except HttpError as error:
        print(F'An error occurred: {error}')
        id = None

    return id

def create_folder(service, name):
    try:
        file_metadata = {
            'name': name,
            'mimeType': 'application/vnd.google-apps.folder'
        }

        # pylint: disable=maybe-no-member
        file = service.files().create(body=file_metadata, fields='id'
                                      ).execute()
        return file.get('id')

    except HttpError as error:
        print(F'An error occurred: {error}')
        return None


def upload_image(service, folder_id, img_dir, name):
    try:
        file_metadata = {
            'name': name, 
            'parents': [folder_id]
        }
        media = MediaFileUpload(img_dir,
                                mimetype='image/jpg')
        # pylint: disable=maybe-no-member
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        service.permissions().create(body={"role":"reader", "type":"anyone"}, fileId=file.get("id")).execute()

        id = file.get("id")

    except HttpError as error:
        print(F'An error occurred: {error}')
        id = None

    return id
