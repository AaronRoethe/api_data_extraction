import logging

logging.basicConfig(filename='app.log',
                    filemode='a',
                    format='%(asctime)s | %(levelname)s | %(message)s',
                    level=logging.INFO,
                    datefmt='%Y-%m-%d %H:%M:%S')

def df_len(name, df):
    logging.info(f'len: {len(df)} \t\t {name}')

def log_everthing(segment,inputs=''):
    logging.info(f"{segment} | {inputs}")