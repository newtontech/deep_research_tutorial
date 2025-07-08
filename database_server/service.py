import sqlite3
import pandas as pd
from typing import List, Dict, Any
from flask import Flask, jsonify, request
import threading
import time

class LocalDatabaseService:
    def __init__(self, db_path: str = "local_data.db"):
        """
        Args:
            db_path: SQLite database file path
        """
        self.db_path = db_path
        self.conn = None
        self.tables = {}
        self._connect()
    
    def _connect(self):
        """Connect to SQLite"""
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row 
    
    def load_table_from_csv(self, csv_path: str, table_name: str, encoding: str = 'utf-8'):
        """
        load data from csv file to database
        Args:
            csv_path: str
            table_name: str
            encoding: str
        """
        try:
            df = pd.read_csv(csv_path, encoding=encoding)
            df.to_sql(table_name, self.conn, if_exists='replace', index=False)
            
            self.tables[table_name] = {
                'fields': list(df.columns),
                'row_count': len(df),
                'source': csv_path
            }
            
            print(f"Loaded '{table_name}': {len(df)} rows")
            print(f"Fields: {list(df.columns)}")
            
        except Exception as e:
            print(f"Failed to load CSV: {e}")
    
    def query(self, sql: str, params: tuple = None) -> List[Dict]:
        """
        Args:
            sql: SQL query statement
            params: query parameters
            
        Returns:
            query results
        """
        try:
            cursor = self.conn.cursor()
            if params:
                cursor.execute(sql, params)
            else:
                cursor.execute(sql)
            
            columns = [description[0] for description in cursor.description]
            results = []
            for row in cursor.fetchall():
                results.append(dict(zip(columns, row)))
            
            return results
        except Exception as e:
            print(f"Failed to query: {e}")
            return []
    
    def get_table_info(self, table_name: str) -> Dict:
        """Get table info"""
        if table_name in self.tables:
            return self.tables[table_name]
        return {}
    
    def list_tables(self) -> List[str]:
        """List all tables"""
        return list(self.tables.keys())
    
    def query_records(self, table_name: str, conditions: List[Dict[str, Any]] = None, 
                      limit: int = 100) -> List[Dict]:
        """
        Search records
        
        Args:
            table_name: table name
            conditions: search conditions, e.g. [{'field': 'name', 'operator': 'eq', 'value': 'John'}, {'field': 'age', 'operator': 'gt', 'value': 25}]
            limit: return record count limit
            
        Returns:
            matched records
        """
        sql = f"SELECT * FROM {table_name}"
        params = []
        
        if conditions:
            where_clauses = []
            for condition in conditions:
                field = condition['field']
                operator = condition['operator']
                value = condition['value']
                if operator == 'like':
                    where_clauses.append(f"{field} LIKE ?")
                    params.append(f"%{value}%")
                elif operator == 'eq':
                    where_clauses.append(f"{field} = ?")
                    params.append(value)
                elif operator == 'gt':
                    where_clauses.append(f"{field} > ?")
                    params.append(value)
                elif operator == 'gte':
                    where_clauses.append(f"{field} >= ?")
                    params.append(value)
                elif operator == 'lt':
                    where_clauses.append(f"{field} < ?")
                    params.append(value)
                elif operator == 'lte':
                    where_clauses.append(f"{field} <= ?")
                    params.append(value)
                elif operator == 'in':
                    value_str = '('+ ','.join(f"'{v}'" for v in value) + ')'
                    where_clauses.append(f"{field} IN {value_str}")
                else:
                    raise ValueError(f"Unsupported operator: {operator}")
            if where_clauses:
                sql += " WHERE " + " AND ".join(where_clauses)
        
        sql += f" LIMIT {limit}"
        return self.query(sql, tuple(params))
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()

def create_api_service(db_service: LocalDatabaseService, port: int = 5000):
    """
    Create Flask API service
    Args:
        db_service: database service instance
        port: service port
    """
    app = Flask(__name__)
    
    @app.route('/tables', methods=['GET'])
    def list_tables():
        return jsonify(db_service.list_tables())
    
    @app.route('/tables/<table_name>/info', methods=['GET'])
    def get_table_info(table_name):
        return jsonify(db_service.get_table_info(table_name))
    
    @app.route('/tables/<table_name>/query', methods=['POST'])
    def query_records(table_name):
        data = request.get_json() or {}
        conditions = data.get('conditions', [])
        limit = data.get('limit', 100)
        
        results = db_service.query_records(table_name, conditions, limit)
        return jsonify(results)
    
    return app

def main():
    db = LocalDatabaseService("my_data.db")
    
    # change to your local files
    db.load_table_from_csv("../data/paper_metadata.csv", "paper_metadata")
    db.load_table_from_csv("../data/paper_text.csv", "paper_text")
    db.load_table_from_csv("../data/paper_figure.csv", "paper_figure")
    db.load_table_from_csv("../data/molecures.csv", "molecures")
    db.load_table_from_csv("../data/solutions.csv", "solutions")
    db.load_table_from_csv("../data/performance.csv", "performance")

    print("available tables:", db.list_tables())
    
    def start_api():
        app = create_api_service(db, port=5002)
        app.run(host='0.0.0.0', port=5002, debug=False)
    
    api_thread = threading.Thread(target=start_api, daemon=True)
    api_thread.start()
    
    print("API服务已启动在 http://localhost:5002")
    print("\n可用的API端点:")
    print("  GET  /tables - 列出所有表")
    print("  GET  /tables/<table_name>/info - 获取表信息")
    print("  POST /tables/<table_name>/query - 搜索记录")

        # 保持服务运行
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n服务已停止")
        db.close()

if __name__ == "__main__":
    main()