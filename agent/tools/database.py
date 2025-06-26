import json
import requests
from typing import Dict, Optional, List

class DatabaseManager:
    """
    A manager for database operations.
    """
    def __init__(self):
        return

    def get_table_fields(self, table_name: str):
        """
        Get the fields of a table
        Args:
            table_name: the name of the table
        Returns:
            A dictionary containing the fields of the table, {'fields': [field_name1, field_name2, ...]}
        """
        fields = set()
        return {'fields': list(fields)}


    def init_get_table_field_info(self):
        """instantiate the get_table_field_info function tool"""
        def get_table_field_info(table_name: str, field_name: str):
            """
            Get the info of a field in a table
            Args:
                table_name: the name of the table
                field_name: the name of the field
            Returns:
                A dictionary containing the info of the field, {'field_info': {field_name: field_info}}
            """
            fields_info = {}
            return {'field_info': fields_info.get(field_name, {})}
        
        return get_table_field_info


    def init_query_table(self):
        """instantiate the query_table function tool"""

        def query_table(table_name: str, filters_json: str, selected_fields: Optional[List[str]] = None, page: Optional[int] = 1, page_size: Optional[int] = 500):
            """
            Query the table
            Args:
                table_name: the name of the table
                filters_json: A JSON formatted string representing the query conditions. IMPORTANT: You must construct the dictionary structure as a valid JSON string.
                The dictionary structure of the filters_json is as follows:
                {
                    'type': 2,
                    'groupOperator': 'and',
                    'sub': [
                        {'type': 1, 'field': 'polymer_type', 'operator': 'like', 'value': 'polyimide'},
                        {'type': 2, 'groupOperator': 'or', 'sub': [
                            {'type': 1, 'field': 'glass_transition_temperature', 'operator': 'lt', 'value': 400},
                        ]}
                    ]
                }
                selected_fields: the fields to include in the result, if None, return all fields
                page: the page number of the query, default is 1
                page_size: the page size of the query, default is 500

            Returns:
                A dictionary containing the result of the query, {'result': [row1, row2, ...], 'row_count': row_count, 'papers': [doi1, doi2, ...], 'paper_count': paper_count}
            """
            rows = []
            row_count = len(rows)
            papers = set([row['doi'] for row in rows if 'doi' in row])
            return {'result': rows, 'row_count': row_count, 'papers': list(papers), 'paper_count': len(papers)}
        return query_table


    def init_fetch_paper_content(self):
        """instantiate the fetch_paper_content function tool"""

        def fetch_paper_content(paper_doi):
            # get paper text
            full_text = None
            
            # get paper figures
            figures = None

            if full_text is None and figures is None:
                return {'error': 'No data found!', 'tool': 'fetch_paper_content'}
            return {'main_txt': full_text, 'figures': figures}
        return fetch_paper_content
