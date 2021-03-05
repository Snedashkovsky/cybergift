from google.cloud import bigquery

from config import GAS_ANALYSIS_DATASET_NAME, FINAL_DATASET_NAME, PROJECT_ID, bq_client, bqstorage_client


def drop_table(table_name, dataset_name=GAS_ANALYSIS_DATASET_NAME):
    """
    Drop a table in a dataset from your project
    :param table_name: The name of the table to be dropped
    :param dataset_name: The dataset name in which the dropped table is located
    :return: True if successful or False otherwise.
    """
    table_ref_1 = bq_client.dataset(dataset_name).table(table_name)
    res = bq_client.delete_table(table_ref_1)  # API request
    if res is None:
        print('Table {}:{} deleted.'.format(dataset_name, table_name))
        return True
    for item in res:
        print(item)
    return False


def create_table(query, table_name, dataset_name=GAS_ANALYSIS_DATASET_NAME):
    """
    Create a table in a dataset from your project
    :param query: SQL query to create a table
    :param table_name: The name of the table to be created
    :param dataset_name: The dataset name in which the created table is located
    :return: True if successful or False otherwise.
    """
    res = bq_client.query(query)
    if res is None:
        print('Table {}:{} created and filled.'.format(dataset_name, table_name))
        return True
    for item in res:
        print(item)
    return False


def create_view(query, view_name, dataset_name=FINAL_DATASET_NAME):
    """
    Create a view in a dataset from your project
    :param query: SQL query to create a view
    :param view_name: The name of the table to be created
    :param dataset_name: The dataset name in which the created view is located
    :return: True if successful or False otherwise.
    """
    view_id = f"{PROJECT_ID}.{dataset_name}.{view_name}"
    view = bigquery.Table(view_id)
    view.view_query = query
    view = bq_client.create_table(view)
    print(f"Created {view.table_type}: {str(view.reference)}")


def get_df(query):
    """
    Get pandas DataFrame by SQL query
    :param query: SQL query to get data for a DataFrame
    :return: DataFrame
    """
    return bq_client.query(query).result().to_dataframe(bqstorage_client=bqstorage_client)
