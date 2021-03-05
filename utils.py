from config import DATASET_NAME, bq_client, bqstorage_client


def drop_table(table_name, dataset_name=DATASET_NAME):
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


def create_table(query, table_name, dataset_name=DATASET_NAME):
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


def get_df(query, columns):
    """
    Get pandas DataFrame by SQL query
    :param query: SQL query to get data for a DataFrame
    :param columns: Name of columns in a DataFrame
    :return: DataFrame
    """
    return bq_client.query(query).result().to_dataframe(bqstorage_client=bqstorage_client)
