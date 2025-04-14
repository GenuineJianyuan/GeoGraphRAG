## Utils for select from S-GMKG (in sqlite3) and retrieval from vector.db
import sqlite3

def select_all_from_db(sql, db_path = "../sgmkg.db"):  ##relative path to sgmkg
    conn = sqlite3.connect(db_path) 
    cursor = conn.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()
    conn.close()
    return results

def select_one_from_db(sql, db_path = "../sgmkg.db"):  ##relative path to sgmkg
    conn = sqlite3.connect(db_path) 
    cursor = conn.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()[0]
    conn.close()
    if result:
        return result[0]
    return None

## interact with schema_vector.db for specific goals
import chromadb
def get_candidate_io_data_entities_from_vectordb(input_list, output_list, top_k = 2):
    chroma_client = chromadb.PersistentClient(path="../schema_vector.db")
    collection = chroma_client.get_collection(name="schema_collection")
    
    input_entity_collection = []
    output_entity_collection = []
    for io_data in input_list:
        results = collection.query(
            query_texts=[io_data], 
            n_results=top_k*3          
        )
        cur_input_matched_ids = []
        for id in results["ids"][0]:
            if len(cur_input_matched_ids)>=top_k:
                break
            if id.startswith("iodata"):
                cur_input_matched_ids.append(id)
        input_entity_collection.append(cur_input_matched_ids)
        
    for io_data in output_list:
        results = collection.query(
            query_texts=[io_data],  
            n_results=top_k*3         
        )
        cur_output_matched_ids = []
        for id in results["ids"][0]:
            if len(cur_output_matched_ids)>=top_k:
                break
            if id.startswith("iodata"):
                cur_output_matched_ids.append(id)
        output_entity_collection.append(cur_output_matched_ids)
        
    return input_entity_collection, output_entity_collection