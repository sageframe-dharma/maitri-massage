#!/usr/bin/env python3
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / 'index.html'

content = INDEX.read_text(encoding='utf-8')

# Ensure we start at the doctype (remove any accidental leading garbage)
doctype_pos = content.find('<!DOCTYPE html>')
html_pos = content.find('<html')
# If there's stray content between <!DOCTYPE html> and <html, remove it
if doctype_pos != -1 and html_pos != -1 and html_pos > doctype_pos:
    # Keep the doctype and the html start, remove whatever is between them
    doctype_text = content[doctype_pos:doctype_pos+len('<!DOCTYPE html>')]
    content = doctype_text + '\n' + content[html_pos:]
elif doctype_pos > 0:
    content = content[doctype_pos:]

# Remove all <style>...</style> blocks (case-insensitive)
content = re.sub(r'<style[\s\S]*?<\/style>', '', content, flags=re.IGNORECASE)

# Remove any <script>...</script> blocks that do NOT have a src attribute
content = re.sub(r'<script\b(?![^>]*\bsrc\b)[\s\S]*?<\/script>', '', content, flags=re.IGNORECASE)

# Ensure external CSS link exists in <head>
head_close = content.lower().find('</head>')
if head_close != -1:
    head = content[:head_close]
    if 'href="styles.css"' not in head and "href='styles.css'" not in head:
        # Insert the link just before </head>
        content = content[:head_close] + '    <link rel="stylesheet" href="styles.css" />\n' + content[head_close:]

# Ensure external script tag just before </body>
body_close = content.lower().rfind('</body>')
if body_close != -1:
    before_body = content[:body_close]
    if 'src="script.js"' not in before_body and "src='script.js'" not in before_body:
        content = content[:body_close] + '    <script src="script.js"></script>\n' + content[body_close:]

# Write back the cleaned index.html
INDEX.write_text(content, encoding='utf-8')

print('index.html cleaned: inline CSS/JS removed and external links ensured')
