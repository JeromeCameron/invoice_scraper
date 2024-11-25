from pdfminer.high_level import extract_text
from pydantic import BaseModel
import re
import os
from pathlib import Path
import pandas as pd
from tqdm import tqdm

# Data model using pydantic
class Invoice(BaseModel):
    invoice_no: str
    reg_id: str | None = None
    date_: str
    mileage: str | None = None
    description: str
    subtotal: str

def get_identifier(extracted_text: str, regx: str) -> str | None:
    """

    :param extracted_text: Text extracted from PDF file
    :param regx: regx pattern
    :return: A string that matches regex pattern.
    """
    try:
        pattern = re.search(regx, extracted_text)
        identifier: str | None = pattern.group().replace(" ", "")
    except AttributeError:
        identifier = None
    return identifier

def check_if_valid_path(text: str) -> bool:
    """

    :param text: user input to check if path
    :return: A boolean
    """
    if os.path.isdir(text):
        return True
    else:
        return False

def get_values(extracted_text: str) -> Invoice:
    """

    :param extracted_text: Text extracted from PDF file
    :return: Invoice details as type Invoice(Data Class)
    """
    # RegX Patterns
    pattern_reg_id: str = r"([A-Z]{2} \d{4})|(\d{4} [A-Z]{2})"  # Licence Plate
    pattern_invoice_no: str = r"SI\d{5}"  # Invoice number
    pattern_money: str = r"(JMD \d*,\d*\.\d*)|(JMD \d*\\.\d*)|(JMD \d*,\d*,\d*\.\d*)" # total spent
    pattern_date: str = r"\d{1,2}\/\d{1,2}\/\d{2,4}"  # invoice date
    pattern_mileage_km: str = r"\d{1,3},\d{1,3} km"  # mileage

    start: int = extracted_text.index("Amount")
    sub_text = extracted_text[start:]

    try:
        end: int = sub_text.index("PARTS")
    except ValueError:
        end: int = sub_text.index("SERVICE")

    result: list[str] = sub_text[:end].splitlines()
    result = list(filter(None, result))
    result.remove("Amount")
    description: str = " ".join([x + " ," for x in result]).title()

    invoice: Invoice = Invoice(
        invoice_no = get_identifier(extracted_text, pattern_invoice_no),
        reg_id = get_identifier(extracted_text, pattern_reg_id),
        date_= get_identifier(extracted_text, pattern_date),
        mileage = get_identifier(extracted_text, pattern_mileage_km),
        description = description,
        subtotal = get_identifier(extracted_text, pattern_money).replace("JMD",""),
    )
    return invoice

def get_invoices(directory: Path) -> list[Invoice]:
    """

    :param directory: Folder containing invoices
    :return: A list of invoice details
    """
    invoices: list = []
    for file in tqdm(os.listdir(directory)):
        if file.endswith(".pdf"):
            extracted_text: str = extract_text(Path(directory) / file)
            invoice: Invoice = get_values(extracted_text)
            invoices.append(invoice)
    return invoices

def main(directory: Path) -> pd.DataFrame:
    """

    :param directory: Folder containing invoices
    :return: Pandas dataframe fo invoices
    """
    invoices: list[Invoice] = get_invoices(directory)
    data = [invoice.model_dump() for invoice in invoices]
    df = pd.DataFrame(data)
    df["date_"] = pd.to_datetime(df["date_"], format="%m/%d/%Y")
    return df

# --------------------------------------------------------------------------------------------
if __name__ == "__main__":

    valid_path: bool = False
    path: Path = Path()

    while not valid_path:
        user_input: str = input("Please enter path to folder with invoices: \n")
        if check_if_valid_path(user_input):
            path = Path(user_input)
            valid_path = True

    invoice_batch = main(path)
    invoice_batch.to_csv(path / "invoices.csv", index=False)