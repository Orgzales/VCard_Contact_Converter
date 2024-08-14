import re
from datetime import datetime

def parse_vcard(text):
    def get_field(pattern, text):
        match = re.search(pattern, text)
        return match.group(1).strip() if match else ''

    last_name = get_field(r'LAST:(.+)', text)
    first_name = get_field(r'FIRST:(.+)', text)
    phone = get_field(r'PHONE.HOME:(.+)', text)
    email = get_field(r'EMAIL:(.+)', text)
    fn = get_field(r'FN:(.+)', text)
    rev = get_field(r'VERSION:(.+)', text)  # Assuming the version line is not used, placeholder if needed

    # Convert REV timestamp if it exists
    rev_match = re.search(r'REV:(.+)', text)
    if rev_match:
        rev_datetime = datetime.fromtimestamp(int(rev_match.group(1)) / 1000.0)
        rev_formatted = rev_datetime.strftime('%Y%m%dT%H%M%SZ')
    else:
        rev_formatted = ''

    # Construct the new vCard format
    return f"""BEGIN:VCARD
VERSION:3.0
N:{last_name};{first_name}
FN:{fn}
TEL;HOME;VOICE:{phone}
EMAIL;PREF;INTERNET:{email}
REV:{rev_formatted}
END:VCARD
"""

def process_vcards(filename):
    with open(filename, 'r') as file:
        data = file.read()
    
    # Split the data by VCARD sections
    vcard_blocks = data.strip().split('\nEND:VCARD\n')
    vcard_blocks = [block + '\nEND:VCARD' for block in vcard_blocks if block.strip()]
    
    # Process each block
    processed_vcards = []
    for block in vcard_blocks:
        if block.startswith('BEGIN:VCARD'):
            processed_vcards.append(parse_vcard(block))
    
    return '\n'.join(processed_vcards)

# File name
filename = 'Text.txt'

# Generate and print the output
output = process_vcards(filename)
print(output)
