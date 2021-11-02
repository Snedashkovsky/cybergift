from google.cloud import bigquery
import pandas as pd

from config import FINAL_DATASET_NAME, PROJECT_ID, bq_client, bqstorage_client


def drop_table(table_name: str, dataset_name: str) -> bool:
    """
    Drop a table in a dataset from your project
    :param table_name: The name of the table to be dropped
    :param dataset_name: The dataset name in which the dropped table is located
    :return: True if successful or False otherwise.
    """
    table_ref_1 = bq_client.dataset(dataset_name).table(table_name)
    try:
        bq_client.delete_table(table_ref_1)
        print(f'Table {dataset_name}:{table_name} has been deleted.')
        return True
    except Exception as e:
        print(f"{e}\nTable {dataset_name}:{table_name} has not been deleted.")
    return False


def create_table(query: str, table_name: str, dataset_name: str, clustering_fields: list = []) -> bool:
    """
    Create a table in a dataset from your project
    :param query: SQL query to create a table
    :param table_name: The name of the table to be created
    :param dataset_name: The dataset name in which the created table is located
    :param clustering_fields: List of fields for clustering
    :return: True if successful or False otherwise.
    """
    table_id = f"{PROJECT_ID}.{dataset_name}.{table_name}"
    if clustering_fields:
        job_config = bigquery.QueryJobConfig(destination=table_id, clustering_fields=clustering_fields)
    else:
        job_config = bigquery.QueryJobConfig(destination=table_id)
    try:
        res = bq_client.query(query, job_config=job_config).result()
        if res.total_rows:
            print(f"Table {dataset_name}:{table_name} has been created and filled {res.total_rows:>,} rows.")
            return True
    except Exception as e:
        print(f"{e}\nTable {dataset_name}:{table_name} has not been created")
    return False


def create_view(query: str, view_name: str, dataset_name: str = FINAL_DATASET_NAME) -> bool:
    """
    Create a view in a dataset from your project
    :param query: SQL query to create a vieThe dataset name in which the created view is located
    :param view_name: The name of the table to be created
    :param dataset_name: The dataset name in which the created view is located
    :return: True if successful or False otherwise.
    """
    view_id = f"{PROJECT_ID}.{dataset_name}.{view_name}"
    view = bigquery.Table(view_id)
    view.view_query = query
    try:
        view = bq_client.create_table(view)
        print(f"View {view.table_type}:{str(view.reference)} has been created.")
        return True
    except Exception as e:
        print(f"{e}\nView {dataset_name}:{view_name} has not been created")
    return False


def create_table_from_df(
        source_df: pd.DataFrame, table_name: str, dataset_name: str, drop_existing_table: bool = True) -> bool:
    """
    Create a table from a Pandas DataFrame
    :param source_df: source Pandas DataFrame
    :param table_name: The name of the table to be created
    :param dataset_name: The dataset name in which the created view is located
    :param drop_existing_table:
    :return: True if successful or False otherwise.
    """
    table_id = f"{PROJECT_ID}.{dataset_name}.{table_name}"
    if drop_existing_table:
        drop_table(table_name, dataset_name)
    try:
        bq_client.load_table_from_dataframe(source_df, table_id).result().done()
        print(f"Table {dataset_name}:{table_name} has been created.")
        return True
    except Exception as e:
        print(f"{e}\nTable {dataset_name}:{table_name} has not been created.")
    return False


def get_df(query: str) -> pd.DataFrame:
    """
    Get Pandas DataFrame by SQL query
    :param query: SQL query to get data for a DataFrame
    :return: DataFrame
    """
    return bq_client.query(query).result().to_dataframe(bqstorage_client=bqstorage_client)
