import html2text

def html_to_markdown(html_content: str) -> str:
    h = html2text.HTML2Text()  
    
    markdown_content = h.handle(html_content)
    
    return markdown_content
