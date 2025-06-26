from .database import DatabaseManager
import json
from pprint import pprint

def test_polymer_db_query_table():
    db_manager = DatabaseManager('polymer_db')
    pprint(db_manager.table_schema)
    query_table = db_manager.init_query_table()
    result = query_table(
        table_name="polym00",
        filters_json=json.dumps({
            "type": 1,
            "field": "doi", 
            "operator": "in",
            "value": ['10.1007/s12221-020-1380-9'],
        })
    )
    pprint(result)


def test_polymer_db_fetch_paper_content():
    db_manager = DatabaseManager('polymer_db')
    fetch_paper_content = db_manager.init_fetch_paper_content()
    result = fetch_paper_content('10.1016/j.polymer.2019.122100')
    print(result)

if __name__ == "__main__":
    test_polymer_db_query_table()
    test_polymer_db_fetch_paper_content()