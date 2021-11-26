import os
import glob
import yaml
import json
from sqlalchemy import create_engine, MetaData
from sqlalchemy_utils import database_exists, create_database
from pmlb import fetch_data
from pmlb import classification_dataset_names, regression_dataset_names


class DictEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__    

DEFAULT_CACHE = '/var/pmlb_cache'
DEFAULT_OUTPUT = '/var/output'
DEFAULT_CONFIG_PATH = '/app/configs'
DEFAULT_LIMIT = 10

ALL_DATASET = [
    *classification_dataset_names, *regression_dataset_names
    ][:DEFAULT_LIMIT]


def pre_populate_cache():
    for data_set in ALL_DATASET:
        print(f"Populating {data_set}...")
        _ = fetch_data(data_set, return_X_y=False,
                       local_cache_dir=DEFAULT_CACHE, dropna=False)


def populate_db(engine):
    for data_set in ALL_DATASET:
        df = fetch_data(data_set, return_X_y=False,
                       local_cache_dir=DEFAULT_CACHE, dropna=False)
        df.to_sql(data_set, con=engine, if_exists='replace')    


def dump_db_schema(engine, output_name):
    m = MetaData(bind=engine)
    m.reflect(engine)
    schema = {}
    for table in m.tables.values():
        schema[table.name] = []
        for column in table.c:
            schema[table.name].append((column.name, column.type))
    output_path = os.path.join(DEFAULT_OUTPUT, output_name)
    with open(output_path, 'w') as f:
        json.dump(schema, f, cls=DictEncoder)


def run_config(config):
    try:
        engine = create_engine(config['dbstring'], echo=False)

        if not database_exists(engine.url):
            create_database(engine.url)
        else:
            # Connect the database if exists.
            engine.connect()

        populate_db(engine)
        dump_db_schema(engine, f"{config['flavor']}.json")
    except Exception:
        pass


def run_configs(config_paths=DEFAULT_CONFIG_PATH):
    print(f"Running configs in {config_paths}/*.yml...")
    for config_path in  glob.glob(f"{config_paths}/*.yml"):
        print(f"Proccessing {config_path}...")
        with open(config_path, "r") as stream:
            try:
                run_config(yaml.safe_load(stream))
            except yaml.YAMLError as exc:
                print(exc)
    print("Done")


if __name__ == "__main__":
    pre_populate_cache()
    run_configs()
