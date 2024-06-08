import markdown
from typing import *

def markdown_parser(md_content: str, heading_color: Optional[str] = '#ffffff') -> str:
    css = f"""
    <style>
        body {{
            background-color: #0d1117;
            color: #c9d1d9;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji';
            line-height: 1.6;
        }}
        pre code, .code-block-md, .code-block-html {{
            background-color: #282c34;
            color: #abb2bf;
            border-radius: 6px;
            padding: 1em;
            overflow-x: auto;
        }}
        h1, h2, h3, h4, h5, h6 {{
            color: {heading_color};
        }}
    </style>
    """

    highlight_links = '''
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.6.0/styles/atom-one-dark.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/5.1.0/github-markdown.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.6.0/highlight.min.js"></script>
    '''

    html_content = markdown.markdown(md_content, extensions=['fenced_code', 'codehilite'])
    html_content = html_content.replace('<pre><code class="', '<pre class="code-block-md"><code class="')

    full_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Markdown Documentation</title>
        {css}
        {highlight_links}
    </head>
    <body>
        {html_content}
        <script>hljs.highlightAll();</script>
    </body>
    </html>
    """

    return full_html
