
import os


from trafilatura import fetch_url, extract

downloaded = fetch_url('https://hub.berachain.com/pools/')

result = extract(downloaded)

print(result)

df = pd.read_csv(io.StringIO(result))

import pandas as pd

raw_list = result.split('\n')


# Extract the header
header_line = [line for line in result.split('\n') if "Pool Composition" in line][0]
columns = [col.strip() for col in header_line.split("|") if col.strip()]

# Extract data rows (after header and separator)
start_index = raw_list.index('|---|---|---|---|---|---|') + 1
data_lines = raw_list[start_index:-1]  # Exclude the '1 of 30' line

# Parse rows into lists
data = [ [cell.strip() for cell in row.split('|') if cell.strip()] for row in data_lines ]

# Create DataFrame
df = pd.DataFrame(data, columns=columns)

# Show the result
print(df)
