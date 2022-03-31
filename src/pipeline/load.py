import sqlalchemy
import pandas as pd
import time

def before_insert(engine:sqlalchemy.engine, remove:str) -> None:
    engine.execute(remove)
    # print(pd.read_sql(lookup, engine))

def sql_insert(engine: sqlalchemy.engine, table:str, load:pd.DataFrame()):
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