import pandas as pd
from traitlets import Enum
from data.constants.raw_data_constants import OngsDatasetCols
from data.constants.segmentation_code import SegmentationCode


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
