import json
import glob
import os
from your_parser_module import DocumentParser  # Import your custom parser

# Initialize your parser
parser = DocumentParser()

# Process all downloaded documents
processed_docs = []

for file_path in glob.glob("edgar_data/*.txt"):
    # Parse file name for metadata
    filename = os.path.basename(file_path)
    parts = filename.replace('.txt', '').split('_')
    ticker = parts[0]
    filing_type = parts[1]
    date = parts[2]
    year = date.split('-')[0]
    
    # Read the file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Parse to structured format (assuming your parser returns a dict)
    parsed_doc = parser.parse(content, output_format="json")
    
    # Add metadata
    parsed_doc['metadata'] = {
        'ticker': ticker,
        'filing_type': filing_type,
        'date': date,
        'year': year
    }
    
    processed_docs.append(parsed_doc)
    
    # Also save individual parsed files
    with open(file_path.replace('.txt', '.json'), 'w', encoding='utf-8') as f:
        json.dump(parsed_doc, f, indent=2)

# Save all processed documents
with open("edgar_data/all_processed_docs.json", 'w', encoding='utf-8') as f:
    json.dump(processed_docs, f, indent=2)
