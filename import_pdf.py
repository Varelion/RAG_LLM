import os
import requests

		# get PDF document path

pdf_path = "human-nutrition-text.pdf"


	# Download PDF

if not os.path.exists(pdf_path):
	print(f"[INFO] File doesn't exist, downloading...")
	# Enter the URL of the PDF
	url = input("Give url for the PDF")
	# The local filename of the downloaded file:
	filename = pdf_path
	# Send a GET request to the URL
	response = requests.get(url)
	# Check if the request was successful
	if response.status_code == 200:
		# open the file and save it
		with open(filename, "wb") as file:
			file.write(response.content)
		print(f"[INFO] The file has been downloaded and saved as {filename}")
	else:
		print(f"[INFO] Filed to download the file. Status code: {response.status_code}")
else:
	print(f"File {pdf_path} exists.")


# Now open it

import PyMuPDF as fitz # requires: !pip install PyMuPDF, see: https://github.com/pymupdf/PyMuPDF
from  tqdm.auto import tqdm # pip instasll tqdm, progress bar


def text_formatter(text:str ) -> str:
	"""Performs minor formatting on text."""
	cleaned_text = text.replace("\n", " ").strip() #Replace newlines with a space, and remove spaces at the end.
	#Potentially more text processing here The better formatted text you pass to an LLM, the better the responses will be.
	return cleaned_text

def open_and_read_pdf(pdf_path: str) -> list[dict]:
	doc = fitz.open(pdf_path)
	pages_and_text= []
	for page_number, page in tqdm(enumerate(doc)): #if doc has 100 pages, page number will start 0,1,2,3...
		text = page.get_text()
		text = text_formatter(text=text)
		pages_and_text.append({"page_number": page_number-41, "page_char_count": len(text),
		"page_word_count": len(text.split(" ")),
		"page_sentence_count_raw": len(text.split(". ")),
		"page_token_count": len(text) / 4, # 1 token = ~4 characters
		"text": text
		})
	return pages_and_text

pages_and_text = open_and_read_pdf(pdf_path=pdf_path)
pages_and_text[:2]
