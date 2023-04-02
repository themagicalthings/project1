***CS5293SP23-Project1*** 

***VAMSI THOKALA***

This Python script redacts sensitive information from text files. The script uses the spacy library to detect entities and regular expressions to redact specific keywords. It allows you to redact names, gender-related words, dates, phone numbers, and addresses.
Parameters

    --names: Redact names
    --genders: Redact gender-related words
    --dates: Redact dates
    --phones: Redact phone numbers
    --address: Redact addresses

***Sample stats output file*** :

The output file will have the following format:

Sample_text.txt.stats

names: 25

genders: 1

dates: 10

phones: 7

addresses: 10


Each line in the output file represents the number of redacted items for each category.

***Usage***

***1.Install the required libraries:***

pip install spacy
pip install en_core_web_md

***2.Run the script with the appropriate flags and arguments:***

python redactor.py --input '*.txt' \ --names --dates --phones --genders --address \ --output 'files/' \ --stats stderr

***Notes***

 1.The script reads input files with the .txt extension in the specified folder.
 2.The output folder will contain redacted text files with the .redacted extension and stats files with the .stats extension. The stats file will contain the number of redacted items for each category.
 3.The --stats flag allows you to output the redaction statistics to the standard error. In this example, we use stderr.

***Functions***

The script contains the following functions:

    redact_names(text: str) -> str: Redacts names from the given text.
    redact_genders(text: str) -> str: Redacts gender-related words from the given text.
    redact_dates(text: str) -> str: Redacts dates from the given text.
    redact_phones(text: str) -> str: Redacts phone numbers from the given text.
    redact_address(text: str) -> str: Redacts addresses from the given text.
    count_redactions(text: str, redacted_text: str) -> Dict[str, int]: Counts the number of redactions made in the given text for each category.
    write_stats(stats: Dict[str, int], file_path: str): Writes the redaction statistics to a file.
    process_files(input_glob: str, output_folder: str, flags: List[str]): Processes the input files, applies redactions based on the flags, and saves the redacted files and statistics in the output folder.
    main(): The main function that parses the command-line arguments and calls the process_files function.

***Requirements***

    Python 3.6 or higher
    spacy library
    en_core_web_md language model

***Limitations***

    The script may not cover all possible cases for redaction.
    The redaction may be affected by the performance of the spacy library's entity recognition and the regular expressions used for redaction.
    The script currently only supports English text.

***Customization***

If you want to customize the script to redact additional information, you can do the following:
1.Add a new function to perform redaction for the new category, similar to the existing redaction functions.
2.Update the count_redactions function to count the redactions for the new category.
3.Update the process_files function to call the new redaction function based on a new flag.
4.Add the new flag to the command-line argument parser in the main function.

***License***

This script is provided under the MIT License. You can use, modify, and distribute the script, but you must include the license notice in all copies or substantial portions of the software.


*** Output ***

<img width="1108" alt="Screenshot 2023-04-02 at 12 15 21 AM" src="https://user-images.githubusercontent.com/115323632/229333271-349bad86-da70-4cb4-93ea-752922698a89.png">

<img width="1108" alt="Screenshot 2023-04-02 at 12 24 10 AM" src="https://user-images.githubusercontent.com/115323632/229333282-bb022dd0-0f71-4480-a1cb-3bb38799d9e2.png">

<img width="1456" alt="Screenshot 2023-04-02 at 12 25 18 AM" src="https://user-images.githubusercontent.com/115323632/229333291-3de4e2e5-343f-4d6a-bcad-86a5991c2f43.png">
