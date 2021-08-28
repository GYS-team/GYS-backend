import sqlite3
import pandas
class DBOperate():
    def __init__(self,db_file_path):
        self._db_file_path=db_file_path
        self.conn=sqlite3.connect(self._db_file_path)
        self.cur=self.conn.cursor()
    def queryall(self,table_name):
        self.cur.execute('select * from '+table_name)
        columns_tuple=self.cur.description
        columns_list=[field_tuple[0] for field_tuple in columns_tuple]
        print(columns_list)
        query_result=self.cur.fetchall()
        return query_result,columns_list
    def to_excel(self,table_name,sheet_name):
        qr,cl=self.queryall(table_name)
        data=pandas.DataFrame(qr,columns=cl)
        print(data)
        with pandas.ExcelWriter('proofs\\proofs\\data.xlsx') as writer:
            data.to_excel(writer,sheet_name=sheet_name)
    def close(self):
        if self.cur is not None:
            self.cur.close()
        if self.conn is not None:
            self.conn.close()
