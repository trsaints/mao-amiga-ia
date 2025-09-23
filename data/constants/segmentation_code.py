from enum import Enum
import pandas as pd
from data.constants.raw_data_constants import OngsDatasetCols

SegmentationCode = Enum('segmentation_code', [
    ('Assistência_Social', 1),
    ('Associações_Patronais_e_Profissionais', 2),
    ('Cultura_e_Recreação', 3),
    ('Desenvolvimento_e_Defesa_de_Direitos_e_Interesses', 4),
    ('Educação_e_Pesquisa', 5),
    ('Outras_Atividades_Associativas', 6),
    ('Religião', 7),
    ('Saúde', 8)
])


def osc_segmentation_codes(entry: pd.Series) -> str:
    """
    Lists all available segmentation codes available in a given entry
    of the OSC dataset.
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
