# loader.py

import os
from typing import List
from langchain_core.documents import Document
from langchain_community.document_loaders import DirectoryLoader, UnstructuredMarkdownLoader
from langchain_community.document_loaders.csv_loader import CSVLoader


def load_documents(data_path: str = "finsolve_docs") -> List[Document]:
    """
    Load markdown and CSV documents from the specified directory
    and add metadata such as role and topic based on filename.

    Args:
        data_path (str): Folder containing markdown and CSV files.

    Returns:
        List[Document]: Combined list of Documents with metadata.
    """

    #  Load Markdown  files with UnstructuredMarkdownLoader
    md_loader = DirectoryLoader(
        path=data_path,
        glob="**/*.md",
        loader_cls=UnstructuredMarkdownLoader
    )
    md_docs = md_loader.load()

    #  Load the single .csv file (hr_data.csv)
    csv_path = os.path.join(data_path, "hr_data.csv")
    csv_docs = []
    if os.path.exists(csv_path):
        csv_loader = CSVLoader(file_path=csv_path)
        csv_docs = csv_loader.load()

    #  Combine both docs
    all_docs = md_docs + csv_docs

    #  Add metadata based on filename
    for doc in all_docs:
        source = doc.metadata.get("source", "").lower()

        # Infer role
        if "finance" in source or "financial" in source:
            doc.metadata["role"] = "finance"
        elif "hr" in source:
            doc.metadata["role"] = "hr"
        elif "marketing" in source:
            doc.metadata["role"] = "marketing"
        elif "engineering" in source:
            doc.metadata["role"] = "engineering"
        elif "employee" in source:
            doc.metadata["role"] = "employee"
        else:
            doc.metadata["role"] = "general"

        # Infer topic from filename
        filename = os.path.basename(source)
        topic = os.path.splitext(filename)[0]
        doc.metadata["topic"] = topic

    return all_docs

docs = load_documents('finsolve_docs')
print(docs[3].page_content)
print(docs[3].metadata)