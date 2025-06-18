import sys
import csv
from image_processor import process_image

def save_elements_to_csv(elements, csv_path):
    """Saves the detected element data to a CSV file."""
    if not elements:
        print("No elements were detected.")
        return

    # Define the headers based on the keys of the first element
    headers = list(elements[0].keys())
    
    try:
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(elements)
        print(f"Successfully wrote {len(elements)} elements to {csv_path}")
    except IOError as e:
        print(f"Error writing to CSV file: {e}")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python main.py <path_to_image>')
        sys.exit(1)

    image_path = sys.argv[1]
    output_csv_path = 'output/elements.csv'

    # 1. Run the simplified detection processor
    detected_elements = process_image(image_path)

    # 2. Save the raw detected data to a CSV
    if detected_elements:
        save_elements_to_csv(detected_elements, output_csv_path)
    else:
        print("Halting execution: No elements detected by the image processor.")
