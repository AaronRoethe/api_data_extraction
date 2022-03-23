import sqlalchemy
from sqlalchemy.engine import URL
import pandas as pd

def sql_engine(server, database) -> sqlalchemy.engine.base.Engine:
    # Enterprise DB to be used
    # pyodbc stuff for MS SQL Server Express
    driver='{SQL Server}'
    trusted_connection='yes'

    # pyodbc connection string
    connection_string = f'DRIVER={driver};SERVER={server};'
    connection_string += f'DATABASE={database};'
    connection_string += f'TRUSTED_CONNECTION={trusted_connection}'

    # create sqlalchemy engine connection URL
    connection_url = URL.create(
        "mssql+pyodbc", query={"odbc_connect": connection_string})
    """ more code not shown that uses pyodbc without sqlalchemy """
    # from sqlalchemy import event
    engine = sqlalchemy.create_engine(connection_url, fast_executemany = True)
    return engine

def load_MSSQL(engine:sqlalchemy.engine.base.Engine, df:pd.DataFrame(), table_name:str, schema:str = 'dbo') -> None:
    try:
        conn = engine.connect()
        print("Connected to server")
    except:
        print("Check connection")
        load_MSSQL(df)
    # form SQL statement
    df.to_sql(table_name, engine, index=False, if_exists="append", schema=schema)
    print("Insert Complete")