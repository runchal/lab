import cv2
import pytesseract
import numpy as np

def detect_elements(image_path):
    """
    Detects elements in a screenshot using Canny edge detection and returns raw data.
    This function focuses only on detection and OCR, not classification.
    """
    try:
        image = cv2.imread(image_path)
        output_image = image.copy()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # 1. Use Canny edge detection
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blur, 50, 150)

        # 2. Use morphological closing to form solid contours
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
        closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

        # 3. Find contours
        contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        elements = []
        element_id = 1
        
        # Filter and sort contours by position
        bounding_boxes = [cv2.boundingRect(c) for c in contours]
        # Skip tiny noise elements
        valid_boxes = [b for b in bounding_boxes if b[2] * b[3] > 2000]
        valid_boxes.sort(key=lambda r: (r[1], r[0])) # Sort top-to-bottom, left-to-right

        for x, y, w, h in valid_boxes:
            # 4. Perform OCR on the region of interest (ROI)
            roi = image[y:y+h, x:x+w]
            text = pytesseract.image_to_string(roi, lang="eng", config="--psm 6").strip()

            elements.append({
                "id": element_id,
                "x": x,
                "y": y,
                "width": w,
                "height": h,
                "text": text
            })
            
            # 5. Draw the box and ID on the output image for visual debugging
            cv2.rectangle(output_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(output_image, str(element_id), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
            element_id += 1

        return output_image, elements

    except Exception as e:
        print(f"An error occurred during element detection: {e}")
        return None, []

def process_image(image_path):
    """
    Main processing function to generate a labeled image and element data.
    """
    output_filename = image_path.split('/')[-1]
    element_output_path = f"output/detected_{output_filename}"

    labeled_image, elements_data = detect_elements(image_path)
    
    if labeled_image is not None:
        cv2.imwrite(element_output_path, labeled_image)
        print(f"Processed detection image saved to: {element_output_path}")

    return elements_data
