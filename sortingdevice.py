import pandas as pd
from urllib.parse import urlparse, urlunparse

file_path = 'originalproquest.csv'
df = pd.read_csv(file_path)

def get_base_url(url):
    try:
        parsed_url = urlparse(url)
        # Split the path into components
        path_parts = parsed_url.path.split('/')
        # Check if 'docview' exists in the path and extract the required part
        if 'docview' in path_parts:
            idx = path_parts.index('docview')
            # Reconstruct the path up to 'docview' and the ID after it
            new_path = '/'.join(path_parts[:idx + 2])
            # Reconstruct the URL with the new path and the original scheme and netloc
            return urlunparse((parsed_url.scheme, parsed_url.netloc, new_path, '', '', ''))
        else:
            # If 'docview' is not in the path, return None or handle as needed
            return None
    except Exception as e:
        return None  # Handle any unexpected errors gracefully
    
df['base_url'] = df['OG Link'].apply(get_base_url)

# Sorting the values by the newly created base urls
df.sort_values(by='base_url', inplace=True)

# Flag duplicates based on the 'base_url' column only
df['duplicated'] = df.duplicated(subset='base_url', keep=False)

# Map the boolean values True/False to Unique and Duplicate
df['duplicated'] = df['duplicated'].map({True: 'Duplicate', False: 'Unique'})

# save output
output_path = 'duplicates.csv'
df.to_csv(output_path, index = False)
print(f"Duplicates saved to {output_path}")
