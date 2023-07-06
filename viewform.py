from __future__ import print_function
from argparse import ArgumentParser
import glob
import random
import time

import sys
sys.path.append('./')
import service
import form

def main():
    parser = ArgumentParser(add_help=True)
    parser.add_argument("--id", type=str, default="none", help="id of the form.")
    parser.add_argument("--noauth_local_webserver", action="store_true", help="true if the server is not local")
    args = parser.parse_args()

    SCOPES = "https://www.googleapis.com/auth/forms.body"

    creds = service.get_creds(SCOPES, 'client_secrets.json', 'token.json')
    forms_service = service.get_forms_service(creds)

    print(form.view_form(forms_service, args.id))

if __name__ == '__main__':
    main()