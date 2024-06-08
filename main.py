from flask import Flask, render_template, request, redirect, url_for, flash

from functions.m2h import markdown_parser
from functions.mv import markdown_viewer
from functions.h2m import html_to_markdown
from functions.create_docs import create_docs

import os
from zipfile import ZipFile
import shutil

app = Flask(__name__)
app.secret_key = b'__!5#y2L"Fhj@k4Q8z\n\xec]/'

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
    docs, error = "", ""
    if request.method == 'POST':
        lib_name = request.form['lib_name']
        zip_file = request.files['dir']

        if zip_file.filename.endswith('.zip'):
            zip_filename = os.path.join('uploads', zip_file.filename)
            zip_file.save(zip_filename)

            extract_dir = os.path.join('uploads', f"{lib_name}_temp")
            os.makedirs(extract_dir, exist_ok=True)

            with ZipFile(zip_filename, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)

            docs = create_docs(lib_name, extract_dir)

            os.remove(zip_filename)
            shutil.rmtree(extract_dir)
            os.remove(f"{lib_name}_documentation.md")
        else:
            error = 'Please upload a zip file.'

    return render_template('create-docs.html', docs=docs, error=error)

app.run(port=5000)
