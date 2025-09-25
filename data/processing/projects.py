from typing import Optional
import pandas as pd

from data.constants.raw_data_constants import ProjectsDatasetCols
from data.processing.data_parser import brazilian_date, to_numeric_value, valid_cnpj


def projects_dataset(source: pd.DataFrame,
                     osc_dataset: pd.DataFrame) -> Optional[pd.DataFrame]:
    """
    Processes a raw dataset of projects, selecting and renaming specific columns. Results are filtered by region.

    Args:
        source (pd.DataFrame): The original dataset containing project information.
        osc_dataset (pd.DataFrame): The processed OSC dataset to filter projects by region.

    Returns:
        pd.DataFrame: The processed dataset, filtered by the "DF" region.
    """

    parsed_statuses = [
        project_status(row[ProjectsDatasetCols.DT_DATA_INICIO_PROJETO],
                       row[ProjectsDatasetCols.DT_DATA_FIM_PROJETO])
        for _, row in source.iterrows()
    ]

    status_df = pd.DataFrame(parsed_statuses, columns=["Status"])

    main_columns = source.copy()

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

    renamed = main_columns_projects(main_columns)

    non_null = (
        pd.concat([renamed.reset_index(drop=True), status_df], axis=1)
        .drop_duplicates(["ID Projeto"])
        .dropna(how="any", subset=["Data de Início"])
        .dropna(how="all", subset=["Total de Beneficiários",
                                   "Valor Captado (R$)",
                                   "Valor Total (R$)"])
    )

    with_num_benefit_total = (
        to_numeric_value(non_null, "Total de Beneficiários", "int")
    )
    with_num_collected_amount = (
        to_numeric_value(with_num_benefit_total, "Valor Captado (R$)", "float")
    )
    with_num_total_amount = (
        to_numeric_value(with_num_collected_amount,
                         "Valor Total (R$)",
                         "float")
    )

    return by_region("DF", with_num_total_amount, osc_dataset)


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


def by_region(region: str,
              projects_dataset: pd.DataFrame,
              osc_dataset: pd.DataFrame) -> Optional[pd.DataFrame]:
    """
    Filters the 'Projects' dataset per region of its responsible OSC

    Args:
        region: the Brazilian Federative Unit (UF) to look for
        osc_dataset: the processed OSC dataset to apply the filter

    Returns:
        DataFrame: the filtered `projects_dataset`, by region
    """
    osc_by_region = osc_dataset.loc[osc_dataset["UF"] == region]

    if osc_by_region.empty:
        return None

    filtered_projects = projects_dataset.loc[
        projects_dataset["CNPJ OSC"].isin(osc_by_region["CNPJ"])
    ]

    if filtered_projects.empty:
        return None

    return filtered_projects


def main_columns_projects(projects_dataset: pd.DataFrame) -> pd.DataFrame:
    """
    Selects and renames the main columns of the 'Projects' dataset.

    Args:
        projects_dataset (pd.DataFrame): The original dataset containing project information. 
    Returns:
        pd.DataFrame: A copy of the dataset with selected and renamed columns.
    """
    main_columns = projects_dataset[
        [ProjectsDatasetCols.ID_PROJETO,
         ProjectsDatasetCols.TX_NOME_PROJETO,
         ProjectsDatasetCols.CD_IDENTIFICADOR_OSC,
         ProjectsDatasetCols.TX_DESCRICAO_PROJETO,
         ProjectsDatasetCols.DT_DATA_INICIO_PROJETO,
         ProjectsDatasetCols.DT_DATA_FIM_PROJETO,
         ProjectsDatasetCols.NR_TOTAL_BENEFICIARIOS,
         ProjectsDatasetCols.NR_VALOR_CAPTADO_PROJETO,
         ProjectsDatasetCols.NR_VALOR_TOTAL_PROJETO]
    ].copy()

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

    return main_columns.rename(columns=columns_map)
