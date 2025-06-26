import json
import requests
from typing import Dict, Optional, List

class DatabaseManager:
    """
    A manager for database operations.
    """
    def __init__(self, base_url: str = "http://localhost:5000"):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.table_schema = {}
        tables = self.session.get(f"{self.base_url}/tables").json()
        for table in tables:
            self.table_schema[table] = self.session.get(f"{self.base_url}/tables/{table}/info").json()

    def init_query_table(self):
        """instantiate the query_table function tool"""

        def query_table(table_name: str, conditions_json: str, page_size: Optional[int] = 100):
            """
            Query the table
            Args:
                table_name: the name of the table
                conditions_json: A JSON formatted string representing the query conditions. 
                The structure of the conditions_json is as follows:
                [
                    {'field': 'polymer_type', 'operator': 'like', 'value': 'polyimide'},
                    {'field': 'glass_transition_temperature', 'operator': 'lt', 'value': 400}
                ]
                page_size: the page size of the query, default is 100

            Returns:
                A dictionary containing the result of the query, {'result': [row1, row2, ...], 'row_count': row_count, 'papers': [doi1, doi2, ...], 'paper_count': paper_count}
            """
            conditions = json.loads(conditions_json)
            rows = self.session.post(f"{self.base_url}/tables/{table_name}/query", json={'conditions': conditions, 'limit': page_size}).json()
            row_count = len(rows)
            papers = set([row['doi'] for row in rows if 'doi' in row])
            paper_count = len(papers)
            return {'result': rows, 'row_count': row_count, 'papers': list(papers), 'paper_count': paper_count}
        return query_table


    def init_fetch_paper_content(self):
        """instantiate the fetch_paper_content function tool"""

        def fetch_paper_content(paper_doi):
            # get paper text
            full_text = None
            condition_json = json.dumps([{'field': 'doi', 'operator': 'eq', 'value': paper_doi}])
            full_text = self.session.post(f"{self.base_url}/tables/paper_text/query", json={'conditions': json.loads(condition_json), 'limit': 1}).json()
            if full_text:
                full_text = full_text[0]['main_txt']
            if full_text is None:
                return {'error': 'No data found!', 'tool': 'fetch_paper_content'}
            return {'main_txt': full_text, 'figures': None}
        return fetch_paper_content
