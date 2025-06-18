import csv
import json

# --- Helper Functions ---

def elements_overlap(elem1, elem2, axis='y'):
    """Check if two elements overlap on a given axis."""
    if axis == 'y':
        return max(elem1['y'], elem2['y']) < min(elem1['y'] + elem1['height'], elem2['y'] + elem2['height'])
    else: # x-axis
        return max(elem1['x'], elem2['x']) < min(elem1['x'] + elem1['width'], elem2['x'] + elem2['width'])

def get_vertical_gap(elem1, elem2):
    """Calculates the vertical gap between two elements."""
    return max(elem1['y'], elem2['y']) - min(elem1['y'] + elem1['height'], elem2['y'] + elem2['height'])


# --- Core Logic ---

def group_elements_into_rows(elements, y_tolerance=20):
    """Groups elements into horizontal rows based on vertical alignment."""
    rows = []
    sorted_elements = sorted(elements, key=lambda e: e['y'])
    
    for element in sorted_elements:
        if element.get('grouped'):
            continue

        # Find a suitable row or create a new one
        best_row = None
        for row in rows:
            # Check if this element is vertically aligned with the row's average y-position
            avg_y = sum(e['y'] for e in row) / len(row)
            if abs(element['y'] - avg_y) < y_tolerance:
                best_row = row
                break
        
        if best_row is not None:
            best_row.append(element)
        else:
            rows.append([element])
        
        element['grouped'] = True
            
    # Sort elements within each row by their x-coordinate
    for row in rows:
        row.sort(key=lambda e: e['x'])
        
    return rows


def main():
    """
    Main function to read raw elements, infer layout, and output a semantic tree.
    """
    input_csv_path = 'output/elements.csv'
    output_json_path = 'output/layout.json'

    try:
        with open(input_csv_path, 'r', encoding='utf-8') as f:
            # Read and convert numeric values
            elements = [{k: (int(v) if v.isdigit() else v) for k, v in row.items()} for row in csv.DictReader(f)]
    except FileNotFoundError:
        print(f"Error: Input file not found at {input_csv_path}")
        return

    # --- Layout Inference ---
    # 1. Group elements into rows
    rows = group_elements_into_rows(elements)
    
    # 2. Build the semantic tree
    # This is a simplified representation for now. We will build on this.
    layout_tree = {
        "type": "body",
        "children": []
    }

    for i, row_elements in enumerate(rows):
        row_node = {
            "type": "row",
            "id": f"row_{i}",
            "children": row_elements
        }
        # A simple heuristic: if a row has multiple items of similar width, it's a grid
        if len(row_elements) > 1:
            avg_width = sum(e['width'] for e in row_elements) / len(row_elements)
            # Check if widths are consistent (within 20%)
            if all(abs(e['width'] - avg_width) / avg_width < 0.2 for e in row_elements):
                row_node["type"] = "grid"
                row_node["columns"] = len(row_elements)
                
        layout_tree["children"].append(row_node)


    # --- Save Output ---
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(layout_tree, f, ensure_ascii=False, indent=4)
    
    print(f"Successfully inferred layout and wrote semantic tree to {output_json_path}")


if __name__ == '__main__':
    main()
