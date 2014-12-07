import re

def strip_whitespace_on_leading_lines(text):
	return re.sub(r'\n\s*', r' ', text).strip()