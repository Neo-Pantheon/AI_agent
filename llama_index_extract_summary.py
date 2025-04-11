

from llama_index.readers.llamaparse import LlamaParseReader
import os
import json

# Step 1: Set your API key
os.environ["LLAMA_CLOUD_API_KEY"] = "xxxxxxxxxxxxx"

# Step 2: Initialize the parser
parser = LlamaParseReader(result_type="markdown")  # or "text"

# Step 3: Load the PDF file
docs = parser.load_data("path/to/HOS_Report.pdf")
parsed_text = docs[0].text

# Step 4: (Optional) Save to file for inspection
with open("parsed_output.md", "w") as f:
    f.write(parsed_text)

# Step 5: Extract structured fields (example: for one daily log)
import re

def extract_summary(text):
    data = {}
    # Extract driver name
    driver_match = re.search(r"# Charles Miller", text)
    if driver_match:
        data["driver_name"] = "Charles Miller"
    # Carrier Name
    carrier_match = re.search(r"Carrier Name:\s*(.*)", text)
    if carrier_match:
        data["carrier_name"] = carrier_match.group(1).strip()
    # ELD Provider
    eld_match = re.search(r"ELD Provider & ID:\s*(.*)", text)
    if eld_match:
        data["eld_provider"] = eld_match.group(1).strip()
    # Driver License
    license_match = re.search(r"Driver License:\s*(.*)", text)
    if license_match:
        data["driver_license"] = license_match.group(1).strip()
    # Distance
    distance_match = re.search(r"Distance:\s*([\d\-]+)\s*km", text)
    if distance_match:
        data["distance_km"] = distance_match.group(1)
    # Rule Set
    ruleset_match = re.search(r"Ruleset:\s*(.*)", text)
    if ruleset_match:
        data["ruleset"] = ruleset_match.group(1).strip()
    # Vehicle
    vehicle_match = re.search(r"Vehicles:\s*(.*)", text)
    if vehicle_match:
        data["vehicle"] = vehicle_match.group(1).strip()
    # Terminal Address
    terminal_match = re.search(r"Home Terminal Address:\s*(.*)", text)
    if terminal_match:
        data["home_terminal"] = terminal_match.group(1).strip()
    return data


extracted_data = extract_summary(parsed_text)
print(json.dumps(extracted_data, indent=2))
