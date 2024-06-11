import os, requests
from flask import jsonify
import qrcode
from PIL import Image
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

load_dotenv()

UPLOAD_AUTHORIZATION_REQUEST_FOLDERS = os.environ.get('UPLOAD_AUTHORIZATION_REQUEST_FOLDERS')
UPLOAD_PURCHASE_REQUEST_FOLDERS = os.environ.get('UPLOAD_PURCHASE_REQUEST_FOLDERS')

def save_files(files, first_name, last_name):
    saved_files = []
    user_folder = os.path.join(UPLOAD_PURCHASE_REQUEST_FOLDERS, f"{first_name}_{last_name}")
    os.makedirs(user_folder, exist_ok=True)

    for file in files:
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(user_folder, filename)
            file.save(file_path)
            saved_files.append(file_path)

    return saved_files

def save_authorization_request_files(files, client_first_name, client_last_name):
    authorization_request_files = []
    user_folder = os.path.join(UPLOAD_AUTHORIZATION_REQUEST_FOLDERS, f"{client_first_name}_{client_last_name}")
    os.makedirs(user_folder, exist_ok=True)

    for file in files:
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(user_folder, filename)
            file.save(file_path)
            authorization_request_files.append(file_path)

    return authorization_request_files

def generate_qr_code(token, first_name, last_name):
    qr_folder = os.path.join(UPLOAD_PURCHASE_REQUEST_FOLDERS, f"{first_name}_{last_name}", "qr_codes")
    os.makedirs(qr_folder)

    qr_path = os.path.join(qr_folder)

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(token)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    
    img.save(qr_path)

    return qr_path
