from flask import Flask, render_template, request
from functions.m2h import markdown_parser
from functions.mv import markdown_viewer

app = Flask(__name__)

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

@app.route('/h2m')
@app.route('/create-docs')
def soon():
    return "Soon ..."

if __name__ == '__main__':
    app.run(port=8767)
