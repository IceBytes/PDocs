import markdown

def markdown_viewer(md_content: str) -> str:
    highlighted_code = markdown.markdown(md_content, extensions=['fenced_code', 'codehilite'])
    return highlighted_code
    