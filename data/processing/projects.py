from typing import Optional
import pandas as pd

from data.constants.raw_data_constants import ProjectsDatasetCols


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
         ProjectsDatasetCols.ID_OSC,
         ProjectsDatasetCols.TX_DESCRICAO_PROJETO,
         ProjectsDatasetCols.DT_DATA_INICIO_PROJETO,
         ProjectsDatasetCols.DT_DATA_FIM_PROJETO,
         ProjectsDatasetCols.NR_TOTAL_BENEFICIARIOS,
         ProjectsDatasetCols.NR_VALOR_CAPTADO_PROJETO,
         ProjectsDatasetCols.NR_VALOR_TOTAL_PROJETO]
    ]

    projects_statuses = [
        project_status(row[ProjectsDatasetCols.DT_DATA_FIM_PROJETO])
        for _, row in source.iterrows()
    ]
    status_df = pd.DataFrame(projects_statuses, columns=["Status"])

    columns_map = {
        ProjectsDatasetCols.ID_PROJETO: "ID Projeto",
        ProjectsDatasetCols.TX_NOME_PROJETO: "Nome",
        ProjectsDatasetCols.ID_OSC: "ID OSC",
        ProjectsDatasetCols.TX_DESCRICAO_PROJETO: "Descrição",
        ProjectsDatasetCols.DT_DATA_INICIO_PROJETO: "Data de Início",
        ProjectsDatasetCols.DT_DATA_FIM_PROJETO: "Data de Término",
        ProjectsDatasetCols.NR_TOTAL_BENEFICIARIOS: "Total de Beneficiários",
        ProjectsDatasetCols.NR_VALOR_CAPTADO_PROJETO: "Valor Captado (R$)",
        ProjectsDatasetCols.NR_VALOR_TOTAL_PROJETO: "Valor Total (R$)"
    }

    renamed = main_columns.rename(columns=columns_map)
    result = pd.concat([renamed.reset_index(drop=True), status_df], axis=1)

    return result


def project_status(project_end_date: Optional[str]) -> str:
    """
    Determines the status of a project based on its end date.

    Args:
        project_end_date (Optional[str]): The end date of the project.

    Returns:
        str: "Ativo" if the project is ongoing, "Encerrado" if it has ended.
    """

    if (project_end_date is None
        or pd.isna(project_end_date)
            or project_end_date.strip() == ""):
        return "Ativo"

    # convert to datetime
    converted_date = pd.to_datetime(project_end_date, errors="coerce")

    if (not pd.isna(converted_date)
            and converted_date < pd.Timestamp.now()):
        return "Encerrado"

    return "Não Informado"
