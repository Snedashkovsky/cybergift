from config import DATASET_NAME, bq_client, bqstorage_client


def drop_table(table_name):
    table_ref_1 = bq_client.dataset(DATASET_NAME).table(table_name)
    bq_client.delete_table(table_ref_1)  # API request
    print('Table {}:{} deleted.'.format(DATASET_NAME, table_name))


def create_table(query, table_name):
    res = bq_client.query(query)
    for item in res:
        print(item)
    print('Table {}:{} created and filled.'.format(DATASET_NAME, table_name))


def get_df(query):
    return bq_client.query(query).result().to_dataframe(bqstorage_client=bqstorage_client)
