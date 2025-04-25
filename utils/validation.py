import re  # Add this import at the top

def validate_data(data):
    errors = []
    
    # Name validation (letters, spaces, hyphens)
    if 'name' in data:
        if not re.match(r'^[A-Za-z\s\-\.]+$', data['name']):
            errors.append("Invalid characters in name")
    
    # Address validation (alphanumeric with basic punctuation)
    if 'address' in data:
        if not re.match(r'^[\w\s\-,\.#]+$', data['address']):
            errors.append("Invalid address format")
    
    # Income validation (numeric with optional commas)
    if 'income' in data:
        if not re.match(r'^\$?[\d,]+(\.\d{2})?$', data['income']):
            errors.append("Invalid income format")
    
    # SSN validation
    if 'ssn' in data:
        if not re.match(r'^\d{3}-\d{2}-\d{4}$', data['ssn']):
            errors.append("SSN must be in XXX-XX-XXXX format")
    
    return errors