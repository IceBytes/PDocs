import os
from zipfile import ZipFile
import magic
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'zip'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def is_safe_file(filepath):
    try:
        filetype = magic.from_file(filepath, mime=True)
        print(f"File type detected: {filetype}")  
        return filetype == 'application/zip'
    except Exception as e:
        print(f"Error checking file type: {e}")
        return False

def is_allowed_filetype(filetype):
    allowed_mime_types = [
        'text/plain',
        'application/json',
        'application/xml',
        'application/x-python-code',
        'text/x-python',
        'text/x-script.python',  
        'application/octet-stream'
    ]
    print(f"Checking file type: {filetype}")  
    return filetype in allowed_mime_types

def is_safe_zip(zip_filename):
    try:
        with ZipFile(zip_filename, 'r') as zip_ref:
            for file_info in zip_ref.infolist():
                print(f"Checking file: {file_info.filename}")  
                if file_info.is_dir():
                    print(f"Ignoring directory: {file_info.filename}")  
                    continue
                if file_info.filename.endswith(('.exe', '.bat', '.sh', '.dll')) or \
                   file_info.filename.startswith(('/', '\\', '..')) or \
                   os.path.isabs(file_info.filename):
                    print("Unsafe file detected based on file extension or path.")  
                    return False
                with zip_ref.open(file_info) as file:
                    filetype = magic.from_buffer(file.read(2048), mime=True)
                    if not is_allowed_filetype(filetype):
                        print(f"Unsafe file type detected: {filetype}")
                        return False
        return True
    except Exception as e:
        print(f"Error checking zip file: {e}")
        return False

def sanitize_filename(filename):
    return secure_filename(filename)
