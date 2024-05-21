import pandas as pd
import json
import re
import spacy
from transformers import pipeline
import yaml
import sys
import os
nlp = spacy.load("en_core_web_sm")

classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def load_data(file_path):
    if file_path.endswith('.csv'):
        return pd.read_csv(file_path)
    elif file_path.endswith('.json'):
        with open(file_path, 'r') as f:
            data = json.load(f)
        return pd.DataFrame(data)
    elif file_path.endswith('.txt'):
        with open(file_path, 'r') as f:
            lines = [line.strip() for line in f if line.strip()]
        return lines
    elif file_path.endswith('.yml') or file_path.endswith('.yaml'):
        with open(file_path, 'r') as f:
            data = yaml.safe_load(f)
        conversations = []
        for conv in data['conversations']:
            dialogues = []
            for dialogue in conv:
                dialogues.append(dialogue)
            conversations.append(dialogues)
        return conversations
    else:
        print("Unsupported file type")
        return None


def is_question(sentence):
    """
    Determine if a sentence is a question using spaCy's POS tagging.
    """
    doc = nlp(sentence)
    if sentence.endswith("?"):
        return True
    return any(token.tag_ == "WP" or token.tag_ == "WRB" for token in doc)

def classify_sentence(sentence):
    """
    Classify a sentence into categories using zero-shot classification.
    Categories can include 'question', 'answer', 'irrelevant', etc.
    """
    categories = ['question', 'answer', 'statement', 'command']
    result = classifier(sentence, categories)
    return result['labels'][0]

def process_data(data):
    processed_data = []
    questions = []

    if isinstance(data, list) and all(isinstance(item, dict) for item in data):
        for item in data:
            question = item.get('question', '').strip()
            answer = item.get('answer', '').strip()
            if question and answer:  #both question and answer are present
                processed_data.append(f"Q: {question} A: {answer}")

    #Unstructured data 
    elif isinstance(data, list):
        flattened_lines = [line for dialogue in data for line in dialogue] if all(isinstance(d, list) for d in data) else data
        
        for line in flattened_lines:
            if line.strip().endswith('?'):
                questions.append(line.strip())
                continue  

            category = classify_sentence(line.strip())
            if category == 'question':
                questions.append(line.strip())
            elif category == 'answer' and questions: 
                qa_pair = "Q: " + questions.pop() + " A: " + line.strip()  
                processed_data.append(qa_pair)

    else:
        print("Unsupported data format for processing.")
    
    return processed_data



def save_data(processed_data, output_path, mode='a'):
    with open(output_path, mode, encoding='utf-8') as f:
        for line in processed_data:
            f.write(line + '\n')

def main():
    if len(sys.argv) > 1:
        input_files = sys.argv[1:]
    else:
        print("Please provide file paths as command line arguments.")
        return

    output_file = '/Users/blakeweiss/Desktop/datalod/processed_data.txt'

    all_processed_data = []
    for file in input_files:
        if not os.path.exists(file):
            print(f"File '{file}' not found.")
            continue

        raw_data = load_data(file)
        if isinstance(raw_data, pd.DataFrame):
            data = raw_data.to_dict('records')
        else:
            data = raw_data

        if data is not None:
            processed_data = process_data(data)
            all_processed_data.extend(processed_data)
    
    save_data(all_processed_data, output_file)

if __name__ == "__main__":
    main()
