from typing import Optional
import pandas as pd

from data.constants.raw_data_constants import ProjectsDatasetCols
from data.processing.data_parser import brazilian_date, valid_cnpj


def projects_dataset(source: pd.DataFrame) -> pd.DataFrame:
    """
    Processes a dataset of projects, selecting and renaming specific columns.

    Args:
        source (pd.DataFrame): The original dataset containing project information.

    Returns:
        pd.DataFrame: The processed dataset with selected and renamed columns.
    """
    main_columns: pd.DataFrame = source[
        [ProjectsDatasetCols.ID_PROJETO,
         ProjectsDatasetCols.TX_NOME_PROJETO,
         ProjectsDatasetCols.CD_IDENTIFICADOR_OSC,
         ProjectsDatasetCols.TX_DESCRICAO_PROJETO,
         ProjectsDatasetCols.DT_DATA_INICIO_PROJETO,
         ProjectsDatasetCols.DT_DATA_FIM_PROJETO,
         ProjectsDatasetCols.NR_TOTAL_BENEFICIARIOS,
         ProjectsDatasetCols.NR_VALOR_CAPTADO_PROJETO,
         ProjectsDatasetCols.NR_VALOR_TOTAL_PROJETO]
    ]

    projects_statuses = [
        project_status(row[ProjectsDatasetCols.DT_DATA_INICIO_PROJETO],
                       row[ProjectsDatasetCols.DT_DATA_FIM_PROJETO])
        for _, row in source.iterrows()
    ]

    status_df = pd.DataFrame(projects_statuses, columns=["Status"])

    main_columns.loc[:, ProjectsDatasetCols.DT_DATA_INICIO_PROJETO] = (
        main_columns[ProjectsDatasetCols.DT_DATA_INICIO_PROJETO]
        .apply(brazilian_date)
    )

    main_columns.loc[:, ProjectsDatasetCols.DT_DATA_FIM_PROJETO] = (
        main_columns[ProjectsDatasetCols.DT_DATA_FIM_PROJETO]
        .apply(brazilian_date)
    )

    main_columns.loc[:, ProjectsDatasetCols.CD_IDENTIFICADOR_OSC] = (
        main_columns[ProjectsDatasetCols.CD_IDENTIFICADOR_OSC]
        .apply(valid_cnpj)
    )

    columns_map = {
        ProjectsDatasetCols.ID_PROJETO: "ID Projeto",
        ProjectsDatasetCols.TX_NOME_PROJETO: "Nome",
        ProjectsDatasetCols.CD_IDENTIFICADOR_OSC: "CNPJ OSC",
        ProjectsDatasetCols.TX_DESCRICAO_PROJETO: "Descrição",
        ProjectsDatasetCols.DT_DATA_INICIO_PROJETO: "Data de Início",
        ProjectsDatasetCols.DT_DATA_FIM_PROJETO: "Data de Término",
        ProjectsDatasetCols.NR_TOTAL_BENEFICIARIOS: "Total de Beneficiários",
        ProjectsDatasetCols.NR_VALOR_CAPTADO_PROJETO: "Valor Captado (R$)",
        ProjectsDatasetCols.NR_VALOR_TOTAL_PROJETO: "Valor Total (R$)"
    }

    renamed = main_columns.rename(columns=columns_map)
    result = (pd.concat([renamed.reset_index(drop=True), status_df], axis=1)
              .drop_duplicates(["ID Projeto"]))

    return result


def project_status(start_date: Optional[str],
                   end_date: Optional[str]) -> str:
    """
    Determines the status of a project based on its end date.

    Args:
        project_end_date (Optional[str]): The end date of the project.

    Returns:
        str: "Ativo" if the project is ongoing, "Encerrado" if it has ended.
    """
    has_start_date = (start_date is not None
                      and str(start_date).strip() != ""
                      and str(start_date).lower() != "nan")

    has_end_date = (end_date is not None
                    and str(end_date).strip() != ""
                    and str(end_date).lower() != "nan")

    if not has_start_date and not has_end_date:
        return "Não Informado"

    # convert to datetime
    parsed_start_date: pd.Timestamp = pd.to_datetime(start_date,
                                                     errors="coerce")
    parsed_end_date: pd.Timestamp = pd.to_datetime(end_date,
                                                   errors="coerce")

    has_started = (parsed_start_date is not None
                   and not pd.isna(parsed_start_date)
                   and parsed_start_date <= pd.Timestamp.now())

    has_ended = (parsed_end_date is not None
                 and not pd.isna(parsed_end_date)
                 and parsed_end_date < pd.Timestamp.now())

    if has_started and has_ended:
        return "Encerrado"

    if has_started and not has_ended:
        return "Ativo"

    return "Não Informado"
