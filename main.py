from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from functions.m2h import markdown_parser
from functions.mv import markdown_viewer
from functions.h2m import html_to_markdown
from functions.create_docs import create_docs
from functions.security import allowed_file, is_safe_file, is_safe_zip, sanitize_filename

import os
import shutil
from zipfile import ZipFile, is_zipfile

app = Flask(__name__)
app.secret_key = os.urandom(24)

UPLOAD_FOLDER = ''
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 

@app.route('/', methods=['GET', 'POST'])
@app.route('/viewer', methods=['GET', 'POST'])
def markdown_view():
    highlighted_code = ""
    if request.method == 'POST':
        md_content = request.form['markdown']
        highlighted_code = markdown_viewer(md_content=md_content)
    return render_template('mv.html', highlighted_code=highlighted_code)

@app.route('/m2h', methods=['GET', 'POST'])
def markdown_to_html():
    html_code = ""
    if request.method == 'POST':
        md_content = request.form['markdown']
        color = request.form['color']
        html_code = markdown_parser(md_content, color)
    return render_template('m2h.html', html_code=html_code)

@app.route('/h2m', methods=['GET', 'POST'])
def h2m():
    markdown_code = ""
    if request.method == 'POST':
        html_content = request.form['html']
        markdown_code = html_to_markdown(html_content)
    return render_template('h2m.html', markdown_code=markdown_code)

@app.route('/create-docs', methods=['GET', 'POST'])
def create_doc():
    docs, error = '', ''
    if request.method == 'POST':
        lib_name = sanitize_filename(request.form['lib_name'])
        zip_file = request.files['dir']
        if zip_file and allowed_file(zip_file.filename):
            filename = secure_filename(zip_file.filename)
            zip_filename = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            zip_file.save(zip_filename)
            
            if is_safe_file(zip_filename) and is_zipfile(zip_filename) and is_safe_zip(zip_filename):
                extract_dir = os.path.join(app.config['UPLOAD_FOLDER'], f"{lib_name}_temp")
                os.makedirs(extract_dir, exist_ok=True)
                try:
                    with ZipFile(zip_filename, 'r') as zip_ref:
                        zip_ref.extractall(extract_dir)
                    docs = create_docs(lib_name, extract_dir)
                except Exception as e:
                    docs = ''
                    error = f"Error processing the zip file: {e}"
                finally:
                    os.remove(zip_filename)
                    shutil.rmtree(extract_dir, ignore_errors=True)
                    if os.path.exists(f"{lib_name}_documentation.md"):
                        os.remove(f"{lib_name}_documentation.md")
            else:
                os.remove(zip_filename)
                error = 'The uploaded zip file is not safe.'
        else:
            error = 'Please upload a valid zip file.'
    return render_template('create-docs.html', docs=docs, error=error)

if __name__ == '__main__':
    app.run(port=5000)
