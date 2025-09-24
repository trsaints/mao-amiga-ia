from typing import Optional, Literal
import pandas as pd
import os
from data.constants.dataset_constants import DATASET_DIR


PortugueseEncoding = Literal["utf-8", "latin1",
                             "cp1252", "iso-8859-15", "mac-roman"]


def to_utf8(dataset_filename: str,
            separator: Optional[str] = None,
            input_encoding: PortugueseEncoding = "utf-8") -> Optional[str]:
    """
    Converts a dataset to UTF-8 encoding and saves it with a new suffix.
    This method accepts various Portuguese encodings as input.

    Args:
        dataset_name (str): The name of the dataset file to convert.
        separator (Optional[str]): The delimiter used in CSV files.
        input_encoding (PortugueseEncoding): The encoding of the input file. Defaults to "utf-8".

    Returns:
        Optional[str]: The path to the converted dataset file, or None if an error occurred.
    """
    try:
        OUTPUT_ENCODING = "utf-8"

        full_path = dataset_path(dataset_filename)

        if full_path is None:
            return None

        filename, extension = os.path.splitext(dataset_filename)
        main_df: pd.DataFrame

        if extension == ".xlsx":
            main_df = pd.read_excel(full_path,
                                    engine="openpyxl")
        elif extension == ".csv":
            main_df = pd.read_csv(full_path,
                                  encoding=input_encoding,
                                  sep=separator if separator else ",",
                                  on_bad_lines="skip")
        else:
            main_df = pd.read_html(full_path,
                                   encoding=input_encoding)[0]

        result_path = output_path(filename)

        main_df.to_csv(result_path,
                       encoding=OUTPUT_ENCODING,
                       sep=";",
                       index=False)

        return result_path

    except Exception as e:
        print(f"Error converting {dataset_filename} to UTF-8: {e}")

        return None


def output_path(dataset_filename: str) -> str:
    """
    Generates the output filename for a UTF-8 converted dataset.

    Args:
        dataset_name (str): The original dataset filename.

    Returns:
        str: The output filename with a UTF-8 suffix.
    """
    OUTPUT_SUFFIX = "_utf8"

    return DATASET_DIR + dataset_filename + OUTPUT_SUFFIX + ".csv"


def dataset_path(dataset_filename: str) -> Optional[str]:
    """
    Generates the full path for a dataset file.

    Args:
        dataset_name (str): The dataset filename.
    Returns:
        str: The full path to the dataset file.
    """
    out_path = DATASET_DIR + dataset_filename
    path_exists = os.path.exists(out_path)

    if not path_exists:
        print(f"File {out_path} does not exist.")

        return None

    return out_path


def brazilian_date(date_str: Optional[str]) -> Optional[str]:
    """
    Converts a date string to the Brazilian date format (dd/mm/yyyy).

    Args:
        date_str (Optional[str]): The input date string.

    Returns:
        Optional[str]: The date in Brazilian format, or None if conversion fails.
    """
    if (date_str is None
        or str(date_str).strip() == ""
            or str(date_str).lower() == "nan"):
        return None

    parsed_date: pd.Timestamp = pd.to_datetime(date_str,
                                               errors="coerce")

    if parsed_date is None or pd.isna(parsed_date):
        return None

    return parsed_date.strftime("%d/%m/%Y")
