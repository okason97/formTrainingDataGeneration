from __future__ import print_function
from argparse import ArgumentParser
import glob
import random
import time

import sys
sys.path.append('./')
import service
import form
import drive

def main():
    parser = ArgumentParser(add_help=True)
    parser.add_argument("--name", type=str, default="img", help="name of the images to be saved.")
    parser.add_argument("--extension", type=str, default=".png", help="file extension.")
    parser.add_argument("--dset", type=str, default="none", help="specify the directory of the folder that contains the images.")
    parser.add_argument("--size", default=20, type=int, help="ammount of images of the form.")
    parser.add_argument("--num", default=1, type=int, help="number of forms.")
    parser.add_argument("--noauth_local_webserver", action="store_true", help="true if the server is not local")
    args = parser.parse_args()

    SCOPES = ['https://www.googleapis.com/auth/drive', "https://www.googleapis.com/auth/forms.body"]

    creds = service.get_creds(SCOPES, 'client_secrets.json', 'token.json')
    drive_service = service.get_drive_service(creds)
    forms_service = service.get_forms_service(creds)

    imgs_path = glob.glob(args.dset + '/**/*.png', recursive=True)
    random.shuffle(imgs_path)


    # Create folder if it does not exist
    folder_id = drive.get_folder_id(drive_service, 'TrainingDataGenerationImages')
    if folder_id is None:
        folder_id = drive.create_folder(drive_service, 'TrainingDataGenerationImages')

    for form_i in range(args.num):
        print("Creating form {}".format(form_i))
        # Save images on google drive and get each image uri
        imgs_uri = []
        for i in range(min(args.size, len(imgs_path)-args.size*form_i)):
            img_id = drive.upload_image(drive_service, folder_id, imgs_path[args.size*form_i+i], "form{}{}{}.png".format(form_i, args.name, i))
            imgs_uri.append("https://drive.google.com/uc?id={}&export=download".format(img_id))

        time.sleep(5)

        form.create_form(forms_service, imgs_uri)

if __name__ == '__main__':
    main()
