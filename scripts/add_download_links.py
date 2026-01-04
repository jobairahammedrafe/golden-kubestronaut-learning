#!/usr/bin/env python3
"""
Add PDF download links to certification pages.
"""
import os
import re
from pathlib import Path

def add_download_links():
    """Add PDF download links to certification pages."""
    # Define certification directories
    cert_dirs = [
        'kcna', 'cka', 'ckad', 'cks', 'kcsa',  # Kubestronaut certs
        'pca', 'cba', 'cca', 'cgoa', 'cnpa', 'cnpe', 'capa'  # Additional certs
    ]
    
    for cert_dir in cert_dirs:
        if not os.path.exists(cert_dir):
            continue
            
        for root, _, files in os.walk(cert_dir):
            for file in files:
                if file.endswith('.md') and file != 'README.md':
                    file_path = os.path.join(root, file)
                    pdf_name = os.path.splitext(file)[0] + '.pdf'
                    
                    # Read the file content
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Skip if download link already exists
                    if '![](' in content and 'Download PDF' in content:
                        continue
                    
                    # Create the download link
                    download_section = f"""
<div class="pdf-download">
  <a href="/pdf/{pdf_name}" class="md-button md-button--primary" download>
    <span class="twemoji">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M5 20h14v-2H5v2zM19 9h-4V3H9v6H5l7 7 7-7z"></path></svg>
    </span>
    Download PDF Version
  </a>
</div>

"""
                    
                    # Add the download section after the first heading
                    lines = content.split('\n')
                    for i, line in enumerate(lines):
                        if line.startswith('# '):
                            lines.insert(i + 1, download_section)
                            break
                    
                    # Write the updated content back to the file
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write('\n'.join(lines))
                    
                    print(f"Added download link to {file_path}")

if __name__ == "__main__":
    add_download_links()
