"""
textloader.py

This module loads a list of text files and returns a flattened list of strings
each corresponding to one of the files.
"""


import os
from typing import List
from typing import AsyncIterator, Iterator

from langchain_core.documents import Document


class SimpleTextLoader:
    """
    NOTE - this is a SIMPLE Text Loader!!
    this class loads a list of text files into a list of list of strings
    Each list will correspond to a single file
    """
    def __init__(self,
                 list_of_text_files: List[str],
                 encoding: str = "utf-8"):
        self.encoding = encoding
        # validate input list
        if isinstance(list_of_text_files, list) and len(list_of_text_files) > 0:
            self.list_of_text_files = list_of_text_files
        else:
            print('ERROR: expecting a non-empty list of text files to be passed in')
            raise Exception
        return
    
    def load_single_text_file(self, filename):
        with open(filename, "r", encoding=self.encoding) as f:
            file_content = f.read()
        return file_content
    
    def load_all_text_files(self):
        list_of_texts = []
        for filename in self.list_of_text_files:
            loaded_text = self.load_single_text_file(filename)
        list_of_texts.append([loaded_text])
        return list_of_texts
    

class LCTextFileLoader:
    """
    NOTE - this is adapted from LangChain.
    This class sets up a CUSTOM Document Loader to load a text file
    into a list of lists of LangChain Document objects.
    Each Document object has attributes including page_content and metadata
    """
    def __init__(self,
                 list_of_text_files: List[str],
                 encoding: str = "utf-8") -> None:
        self.encoding = encoding
        # validate input list
        if isinstance(list_of_text_files, list) and len(list_of_text_files) > 0:
            self.list_of_text_files = list_of_text_files
        else:
            print('ERROR: expecting a non-empty list of text files to be passed in')
            raise Exception
        return

    def load_single_text(self, filename):
        """
        A loader that reads a file.
        """
        with open(filename, "r", encoding=self.encoding) as f:
            file_content = f.read()
        return Document(
            page_content=file_content,
            metadata={"document_number": self.doc_number, "source": filename},
        )
    
    def load_all_text_files(self):
        list_of_texts = []
        self.doc_number = 0
        for filename in self.list_of_text_files:
            loaded_text = self.load_single_text(filename)
            self.doc_number += 1
        list_of_texts.append([loaded_text])
        return list_of_texts
