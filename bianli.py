import json
import pickle
from tqdm import tqdm
import json
import os
import pandas as pd
import random
import re
from datasets import load_dataset

def read_json(directory):
    data = []
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r') as f:
                file_data = json.load(f)
                data.extend(file_data)
    return data

def write_jsonl(JSON_file, outfile_path):
    with open(outfile_path, 'w') as outfile:
        for entry in JSON_file:
            json.dump(entry, outfile)
            outfile.write('\n')

if __name__ == "__main__":
    Gutenberg_data_jsonl = []
    dataset = load_dataset("SaylorTwift/Gutenberg", split="train", streaming=True)
    for item in dataset:
        Gutenberg_data_jsonl.append(item)
    write_jsonl(Gutenberg_data_jsonl, outfile_path = "/export/project/hyangby/.cache/huggingface/datasets/downloads.jsonl")
