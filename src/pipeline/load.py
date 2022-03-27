from dataclasses import dataclass, field
import sqlalchemy
from sqlalchemy.engine import URL
import pandas as pd
import time


@dataclass
class MSSQL:
    server  : str
    database: str
    driver  : str = "ODBC Driver 17 for SQL Server"
    engine  : sqlalchemy.engine = field(init=False)

    def __post_init__(self) -> None:
        self.engine = sqlalchemy.create_engine(
        f"mssql+pyodbc://{self.server}/{self.database}?driver={self.driver}", fast_executemany=True)

def sql_insert(load, server: MSSQL, table):
    # ask to go forward with insert
    if input("Enter(y/n): ") == 'y':
        pass
    else:
        raise SystemExit
    ### Load file ###
    t0 = time.time()
    ### Add today's file #
    load.to_sql(table, server.engine, index=False, if_exists="append")
    print(f'Inserts completed in {time.time() - t0:.2f} seconds.')