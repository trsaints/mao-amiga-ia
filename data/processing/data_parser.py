from typing import Optional
import pandas as pd

from data.constants.dataset_constants import DATASET_DIR


def to_utf8(dataset_name: str) -> Optional[str]:
    """
    Converts a dataset to UTF-8 encoding and saves it with a new suffix.
    This method assumes the input dataset is encoded in 'cp860', which is the encoding for legacy systems for the Portuguese language.

    Args:
        dataset_name (str): The name of the dataset file to convert.

    Returns:
        Optional[str]: The path to the converted dataset file, or None if an error occurred.
    """
    try:
        INPUT_ENCODING = "cp860"
        OUTPUT_ENCODING = "utf-8"

        main_df = pd.read_csv(DATASET_DIR + dataset_name,
                              encoding=INPUT_ENCODING, sep=";",
                              on_bad_lines="skip")
        output_dir = output_name(dataset_name)

        main_df.to_csv(output_dir,
                       encoding=OUTPUT_ENCODING,
                       sep=";",
                       index=False)

        return output_dir
    except Exception as e:
        print(f"Error converting {dataset_name} to UTF-8: {e}")
        return None


def output_name(dataset_name: str) -> str:
    """
    Generates the output filename for a UTF-8 converted dataset.

    Args:
        dataset_name (str): The original dataset filename.

    Returns:
        str: The output filename with a UTF-8 suffix.
    """
    OUTPUT_SUFFIX = "_utf8"
    return DATASET_DIR + dataset_name + OUTPUT_SUFFIX + ".csv"
