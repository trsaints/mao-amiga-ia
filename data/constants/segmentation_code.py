from enum import Enum
import pandas as pd
from data.constants.raw_data_constants import OngsDatasetCols

SEGMENTATION_CODE = Enum('segmentation_code', [
    ('Assistência_Social', 1),
    ('Associações_Patronais_e_Profissionais', 2),
    ('Cultura_e_Recreação', 3),
    ('Desenvolvimento_e_Defesa_de_Direitos_e_Interesses', 4),
    ('Educação_e_Pesquisa', 5),
    ('Outras_Atividades_Associativas', 6),
    ('Religião', 7),
    ('Saúde', 8)
])


def osc_segmentation_codes(entry: pd.Series) -> list[str]:
    """
    Lists all available segmentation codes available in a given entry
    of the OSC dataset.
    """
    enum_codes = []

    if entry[OngsDatasetCols.AREA_ASSISTENCIA_SOCIAL] == 1:
        enum_codes.append(SEGMENTATION_CODE.Assistência_Social)

    if entry[OngsDatasetCols.AREA_ASSOCIACOES_PATRONAIS_E_PROFISSIONAIS] == 1:
        enum_codes.append(
            SEGMENTATION_CODE.Associações_Patronais_e_Profissionais)

    if entry[OngsDatasetCols.AREA_CULTURA_E_RECREACAO] == 1:
        enum_codes.append(SEGMENTATION_CODE.Cultura_e_Recreação)

    if entry[OngsDatasetCols.AREA_DESENVOLVIMENTO_E_DEFESA_DE_DIREITOS_E_INTERESSES] == 1:
        enum_codes.append(
            SEGMENTATION_CODE.Desenvolvimento_e_Defesa_de_Direitos_e_Interesses)

    if entry[OngsDatasetCols.AREA_EDUCACAO_E_PESQUISA] == 1:
        enum_codes.append(SEGMENTATION_CODE.Educação_e_Pesquisa)

    if entry[OngsDatasetCols.AREA_OUTRAS_ATIVIDADES_ASSOCIATIVAS] == 1:
        enum_codes.append(SEGMENTATION_CODE.Outras_Atividades_Associativas)

    if entry[OngsDatasetCols.AREA_RELIGIAO] == 1:
        enum_codes.append(SEGMENTATION_CODE.Religião)

    if entry[OngsDatasetCols.AREA_SAUDE] == 1:
        enum_codes.append(SEGMENTATION_CODE.Saúde)

    result = [code.name for code in enum_codes]

    return result
