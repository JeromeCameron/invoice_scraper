# Invoice Scraper 🦾
Invoice Scraper is a Python package that extracts data from PDF invoice 
files in a given folder and outputs the data in a CSV file. 
This tool is designed to automate the extraction process.
***
### Features
- Automatically scans a specified folder for PDF files.
- Extracts structured data such as invoice number, date, amount etc.
- Outputs the extracted data into a clean CSV file.
- Handles multiple invoices in one run.

### Installation
Install the package using pip:
```bash 
$ git clone https://github.com/JeromeCameron/invoice_scraper
$ cd invoice_scraper
$ pip install -r requirements.txt
```

### Usage
Command-Line Interface (CLI)
```bash
$ python invoice_scraper.py
Please enter path to folder with invoices:
Enter path to file
```
csv file is outputted to folder containing invoices

### Requirements
Python 3.8+

Required Python libraries (installed via requirements.txt):
- pdfminer.six (for PDF parsing)
- pandas (for CSV handling)
- pydantic (for data model)
- tqdm (for progress tracker)
- os, re, and other standard libraries

***

####  Note
This package is tailored to ***work with a specific invoice layout***. 
If your invoices use a different structure, the code will need to 
be modified to adapt to your format. To customize the scraper for 
other layouts, you'll need to update the parsing logic in the 
code to match the unique structure of your invoices. 