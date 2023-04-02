import re
import os
import glob
import spacy
import en_core_web_md
from typing import List, Dict
import argparse

nlp = en_core_web_md.load()

def redact_names(text: str) -> str:
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ in ['PERSON', 'ORG', 'GPE']:
            text = text.replace(ent.text, '█' * len(ent.text))
    return text

def redact_genders(text: str) -> str:
    gender_terms = ['him', 'her', 'father', 'mother', 'male', 'female', 'wife', 'husband', 'king', 'queen', 'feminine', 'masculine', 'father', 'brother', 'brother-in-law', 'sister', 'girl', 'boy', 'man', 'woman', 'women', 'men', 'actress', 'waitress', 'daughter', 'son', 'bride', 'groom', 'uncle', 'aunt', 'mom', 'mother', 'papa', 'niece', 'nephew']
    return re.sub(r'\b(?:' + '|'.join(gender_terms) + r')\b', '█', text, flags=re.IGNORECASE)

def redact_dates(text: str) -> str:
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == 'DATE':
            text = text.replace(ent.text, '█' * len(ent.text))
    return text

def redact_phones(text: str) -> str:
    return re.sub(r'\b(?:\d{2,4}[-\s.]?){2,3}\d\b', '█', text)

def redact_address(text: str) -> str:
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == 'GPE':
            text = text.replace(ent.text, '█' * len(ent.text))
    return text

def count_redactions(text: str, redacted_text: str) -> Dict[str, int]:
    redactions = {'names': 0, 'genders': 0, 'dates': 0, 'phones': 0, 'addresses': 0}

    original_doc = nlp(text)
    redacted_doc = nlp(redacted_text)

    redactions['names'] = len([ent for ent in original_doc.ents if ent.label_ == 'PERSON'])
    redactions['genders'] = len(re.findall(r'\b(?:' + '|'.join(['him', 'her', 'father', 'mother']) + r')\b', text, flags=re.IGNORECASE))
    redactions['dates'] = len([ent for ent in original_doc.ents if ent.label_ == 'DATE'])
    redactions['phones'] = len(re.findall(r'\b(?:\d{2,4}[-\s.]?){2,3}\d\b', text))
    redactions['addresses'] = len([ent for ent in original_doc.ents if ent.label_ == 'GPE'])

    return redactions

def write_stats(stats: Dict[str, int], file_path: str):
    with open(file_path, 'w', encoding='utf-8') as f:
        for key, value in stats.items():
            f.write(f"{key}: {value}\n")

def process_files(input_glob: str, output_folder: str, flags: List[str]):
    file_paths = glob.glob(input_glob)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for file_path in file_paths:
        try:
            with open(file_path, 'r', encoding='utf-8') as input_file:
                text = input_file.read()
                redacted_text = text
                
                for flag in flags:
                    try:
                        if flag == '--names':
                            redacted_text = redact_names(redacted_text)
                        elif flag == '--genders':
                            redacted_text = redact_genders(redacted_text)
                        elif flag == '--dates':
                            redacted_text = redact_dates(redacted_text)
                        elif flag == '--phones':
                            redacted_text = redact_phones(redacted_text)
                        elif flag == '--address':
                            redacted_text = redact_address(redacted_text)
                    except Exception as e:
                        print(f"Error redacting '{flag[2:]}' in '{file_path}': {e}")

                output_path = os.path.join(output_folder, os.path.basename(file_path) + '.redacted')
                with open(output_path, 'w', encoding='utf-8') as output_file:
                    output_file.write(redacted_text)

                stats = count_redactions(text, redacted_text)
                stats_path = os.path.join(output_folder, os.path.basename(file_path) + '.stats')
                write_stats(stats, stats_path)

        except Exception as e:
            print(f"Error processing file '{file_path}': {e}")

def main():
    parser = argparse.ArgumentParser(description='Redact sensitive information from text files.')
    parser.add_argument('--input', type=str, required=True, help="Input file pattern, e.g., '*.txt'")
    parser.add_argument('--names', action='store_true', help='Redact names')
    parser.add_argument('--dates', action='store_true', help='Redact dates')
    parser.add_argument('--phones', action='store_true', help='Redact phone numbers')
    parser.add_argument('--genders', action='store_true', help='Redact gender-related words')
    parser.add_argument('--address', action='store_true', help='Redact addresses')
    parser.add_argument('--output', type=str, required=True, help='Output folder path')
    parser.add_argument('--stats', type=str, choices=['stderr'], help='Output stats to standard error')

    args = parser.parse_args()

    flags = []
    if args.names:
        flags.append('--names')
    if args.dates:
        flags.append('--dates')
    if args.phones:
        flags.append('--phones')
    if args.genders:
        flags.append('--genders')
    if args.address:
        flags.append('--address')

    process_files(args.input, args.output, flags)

    if args.stats == 'stderr':
        import sys
        for file_path in glob.glob(os.path.join(args.output, '*.stats')):
            with open(file_path, 'r', encoding='utf-8') as f:
                sys.stderr.write(f"\n{os.path.basename(file_path)}\n")
                sys.stderr.write(f.read())

if __name__ == "__main__":
    main()

