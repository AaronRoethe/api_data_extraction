from dataclasses import dataclass, field
import sqlalchemy
from sqlalchemy.engine import URL
import pandas as pd
import time



def sql_insert(load, engine: sqlalchemy.engine, table):
    # ask to go forward with insert
    if input("Enter(y/n): ") == 'y':
        pass
    else:
        raise SystemExit
    ### Load file ###
    t0 = time.time()
    ### Add today's file #
    load.to_sql(table, engine, index=False, if_exists="append")
    print(f'Inserts completed in {time.time() - t0:.2f} seconds.')