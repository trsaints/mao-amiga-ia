from typing import Optional
import pandas as pd
import os

from zmq import Enum

from data.constants.dataset_constants import DATASET_DIR
from data.constants.raw_data_constants import OngsDatasetCols
from data.constants.segmentation_code import SegmentationCode


def to_utf8(dataset_filename: str) -> Optional[str]:
    """
    Converts a dataset to UTF-8 encoding and saves it with a new suffix.
    This method assumes the input dataset is encoded in 'latin1', which is the encoding for legacy systems for the Portuguese language.

    Args:
        dataset_name (str): The name of the dataset file to convert.

    Returns:
        Optional[str]: The path to the converted dataset file, or None if an error occurred.
    """
    try:
        INPUT_ENCODING = "latin1"
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
                                  encoding=INPUT_ENCODING, sep=";",
                                  on_bad_lines="skip")
        else:
            main_df = pd.read_html(full_path,
                                   encoding=INPUT_ENCODING)[0]

        result_path = output_path(filename)

        main_df.to_csv(result_path,
                       encoding=OUTPUT_ENCODING,
                       sep=";",
                       index=False)

        return result_path

    except Exception as e:
        print(f"Error converting {dataset_filename} to UTF-8: {e}")

        return None


def osc_dataset(dataset: pd.DataFrame) -> pd.DataFrame:
    """
    Generates a processed OSC dataset with selected and renamed columns.

    Args:
        osc_dataset (pd.DataFrame): The original OSC dataset.

    Returns:
        pd.DataFrame: The processed OSC dataset with selected and renamed columns.
    """

    main_columns: pd.DataFrame = dataset[[OngsDatasetCols.CNPJ,
                                          OngsDatasetCols.TX_RAZAO_SOCIAL_OSC,
                                          OngsDatasetCols.MUNICIPIO_NOME,
                                          OngsDatasetCols.UF_SIGLA]]

    # CNPJ column must be a string of 14 digits
    main_columns.loc[:, OngsDatasetCols.CNPJ] = (main_columns[OngsDatasetCols.CNPJ]
                                                 .astype(str)
                                                 .str
                                                 .zfill(14))

    columns_map = {
        OngsDatasetCols.CNPJ: "CNPJ",
        OngsDatasetCols.TX_RAZAO_SOCIAL_OSC: "Razão Social",
        OngsDatasetCols.MUNICIPIO_NOME: "Município",
        OngsDatasetCols.UF_SIGLA: "UF"
    }

    renamed = main_columns.rename(columns=columns_map)
    area_codes = [osc_segmentation_codes(row) for _, row in dataset.iterrows()]
    area_codes_df = pd.DataFrame(area_codes)
    result = pd.concat([renamed.reset_index(drop=True), area_codes_df], axis=1)

    return result


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


def osc_segmentation_codes(entry: pd.Series) -> str:
    """
    Lists all available segmentation codes available in a given entry
    of the OSC dataset.

    Args:
        entry (pd.Series): A row entry from the OSC dataset.

    Returns:
        str: A comma-separated string of segmentation code names.
    """
    def parse_code(value: str) -> int:
        try:
            return int(entry[value])
        except (ValueError, TypeError):
            return 0

    enum_codes: list[Enum] = []

    if parse_code(OngsDatasetCols.AREA_ASSISTENCIA_SOCIAL) == 1:
        enum_codes.append(SegmentationCode.Assistência_Social)

    if parse_code(OngsDatasetCols.AREA_ASSOCIACOES_PATRONAIS_E_PROFISSIONAIS) == 1:
        enum_codes.append(
            SegmentationCode.Associações_Patronais_e_Profissionais)

    if parse_code(OngsDatasetCols.AREA_CULTURA_E_RECREACAO) == 1:
        enum_codes.append(SegmentationCode.Cultura_e_Recreação)

    if parse_code(OngsDatasetCols.AREA_DESENVOLVIMENTO_E_DEFESA_DE_DIREITOS_E_INTERESSES) == 1:
        enum_codes.append(
            SegmentationCode.Desenvolvimento_e_Defesa_de_Direitos_e_Interesses)

    if parse_code(OngsDatasetCols.AREA_EDUCACAO_E_PESQUISA) == 1:
        enum_codes.append(SegmentationCode.Educação_e_Pesquisa)

    if parse_code(OngsDatasetCols.AREA_OUTRAS_ATIVIDADES_ASSOCIATIVAS) == 1:
        enum_codes.append(SegmentationCode.Outras_Atividades_Associativas)

    if parse_code(OngsDatasetCols.AREA_RELIGIAO) == 1:
        enum_codes.append(SegmentationCode.Religião)

    if parse_code(OngsDatasetCols.AREA_SAUDE) == 1:
        enum_codes.append(SegmentationCode.Saúde)

    code_names = [code.name.replace("_", " ") for code in enum_codes]

    return ", ".join(code_names)
