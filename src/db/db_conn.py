import sqlite3
import csv


def get_connection():
    connection = sqlite3.connect("./data/lyrion_disk0.db")
    return connection

def create_db():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS lyrion")
    cursor.execute("CREATE TABLE lyrion (nfc_id TEXT, search_type TEXT, search_str TEXT)")
    connection.commit()
    connection.close()
    
def load_db_from_csv(filepath = "./data/lyrion_disk0.csv"):
    connection = get_connection()
    cursor = connection.cursor()
    with open(filepath,'r') as fin: # `with` statement available in 2.5+
        # csv.DictReader uses first line in file for column headings by default
        dr = csv.DictReader(fin) # comma is default delimiter
        to_db = [(i['nfc_id'], i['search_type'], i['search_str']) for i in dr]
    cursor.executemany("INSERT into lyrion (nfc_id, search_type, search_str) values (?,?,?);", to_db)
    connection.commit()
    connection.close()


def query_id_from_db(id): 
    connection = get_connection()
    cursor = connection.cursor()
    query = f"SELECT * from lyrion where nfc_id='{id}'" 
    results = cursor.execute(query).fetchall()
    if len(results) == 0:
        print(f'cannot find nfc tag id {id}')
        
    elif len(results)>1:
        print("more than 1 match for nfc_id. please check db.")
        print(results)
    connection.close()
    
    return results[0]
    
if __name__ == "__main__":
    create_db()
    load_db_from_csv()
    print("loaded data into db")
    connection = get_connection()
    cursor = connection.cursor()
    print(cursor.execute("select * from lyrion").fetchall())
    connection.close()