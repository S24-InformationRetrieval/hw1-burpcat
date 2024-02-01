from elasticsearch import Elasticsearch
from pathlib import Path
import re
from pprint import pprint
import json

from tokenizer import porter_processing,porter_mod_processing_one

base_string = "/home/burpcat/Documents/assignments/ir/hw1-burpcat/IR_data/AP_DATA/ap89_collection"

index_dict = {}

def pathOpener():
    file_path = base_string  # Replace with the directory path you want to list files from

    try:
        directory = Path(file_path)
        files = [file for file in directory.iterdir() if file.is_file()]
        main_list = [file.name for file in files]
        return main_list
    except FileNotFoundError:
        print(f"The directory '{file_path}' was not found.")

def tagMatcher(text_block):

    # Define regular expressions for tags
    docno_pattern = r'<DOCNO>(.*?)</DOCNO>'
    text_pattern = r'<TEXT>(.*?)</TEXT>'

    # Find and extract all DOCNO and TEXT contents
    docno_matches = re.finditer(docno_pattern, text_block, re.DOTALL)
    text_matches = re.finditer(text_pattern, text_block, re.DOTALL)


    # Iterate through the matches and print the contents
    for docno_match, text_match in zip(docno_matches, text_matches):
        docno = docno_match.group(1).replace(' ', '')
        text = text_match.group(1).replace('\n', ' ')
        # text = porter_mod_processing_one(text)
        index_dict.update({docno:text})

    
def contentLister(file_lists):
    
    for ele in file_lists:
        file_path = f"{base_string}/{ele}"
        try:
            with open(file_path, 'r',encoding="ISO-8859-1") as file:
                # Read the entire file into a string
                file_contents = file.read()
                tagMatcher(file_contents)
        except FileNotFoundError:
            print(f"The file '{file_path}' was not found.")
        except IOError:
            print(f"An error occurred while reading the file '{file_path}'.")

def start_file_parse():
    
    file_lists = pathOpener()
    contentLister(file_lists)

    with open('output.json', 'w') as json_file:
        json.dump(index_dict, json_file)
    return index_dict
