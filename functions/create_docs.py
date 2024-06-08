from docsgen import DocsGen

def create_docs(lib_name: str, dir: str) -> None:
    engine = DocsGen(lib_name, dir)
    engine.write_documentation()
    docs = open(f"{lib_name}_documentation.md", "r").read()
    return docs