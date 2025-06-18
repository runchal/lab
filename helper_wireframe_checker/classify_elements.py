import csv

CTA_KEYWORDS = ['learn more', 'get started', 'submit', 'rent', 'shop', 'rent now']

def classify_element(element, page_width):
    """
    Classifies an element based on a set of rules and heuristics.
    
    Args:
        element (dict): A dictionary representing a single detected element.
        page_width (int): The total width of the original image.
        
    Returns:
        str: The classified type of the element.
    """
    # Convert string values from CSV to int/float for calculations
    x, y, w, h = int(element['x']), int(element['y']), int(element['width']), int(element['height'])
    text = element['text'].lower()
    
    # Rule 1: Structural Elements (Sections)
    # A section is very wide and reasonably tall.
    if w > page_width * 0.8 and h > 150:
        return 'section'

    # Rule 2: CTA Keywords for Buttons (High Confidence)
    if any(keyword in text for keyword in CTA_KEYWORDS):
        return 'button'
        
    # Rule 3: Cards
    # Cards have a typical aspect ratio and size.
    aspect_ratio = w / h
    if 250 < w < 650 and 300 < h < 600 and 0.5 < aspect_ratio < 1.5:
        return 'card'

    # Rule 4: Headings
    # Headings are prominent, not too many words.
    if h > 50 and w > 100 and len(text.split()) < 10 and text:
        return 'h1' if h > 80 else 'h2'

    # Rule 5: Small icon-like elements with no text
    if w < 60 and h < 60 and not text:
        return 'icon'

    # Rule 6: Default to text/paragraph
    if text:
        return 'p' # 'p' for paragraph or general text

    # Default fallback
    return 'container'

def main():
    """
    Main function to read, classify, and write element data.
    """
    input_csv_path = 'output/elements.csv'
    output_csv_path = 'output/elements_tagged.csv'
    # We assume a standard page width for classification rules, ~1366px is common
    PAGE_WIDTH = 1366 

    try:
        with open(input_csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            elements = list(reader)
    except FileNotFoundError:
        print(f"Error: Input file not found at {input_csv_path}")
        print("Please run the detection script (main.py) first.")
        return

    tagged_elements = []
    for element in elements:
        # Create a copy to avoid modifying the original dict while iterating
        new_element = element.copy()
        element_type = classify_element(new_element, PAGE_WIDTH)
        new_element['type'] = element_type
        tagged_elements.append(new_element)

    # Write the new tagged data to the output file
    if tagged_elements:
        headers = list(tagged_elements[0].keys())
        # Ensure 'type' is one of the first columns for readability
        if 'type' in headers:
            headers.insert(1, headers.pop(headers.index('type')))

        with open(output_csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(tagged_elements)
        print(f"Successfully classified and wrote {len(tagged_elements)} elements to {output_csv_path}")

if __name__ == '__main__':
    main()
