## utils for path retrieval as well as its nodes(entities)

from collections import deque
from db_utils import select_all_from_db, select_one_from_db, get_candidate_io_data_entities_from_vectordb


def get_candidate_io_data_entities(input_list, output_list, top_k = 2):
    return get_candidate_io_data_entities_from_vectordb(input_list, output_list, top_k)

def retrieve_path_by_bfs(source_id, target_id, max_paths=10):
    sql = """
        SELECT output_entity_id, input_entity_id, relation_type 
        FROM schema_relation
        WHERE relation_type IN ('invoke', 'transfer')
    """
    relations = select_all_from_db(sql)

    # build adjacency graph
    graph = {}
    relation_types = {}
    for output_id, input_id, rel_type in relations:
        if output_id not in graph:
            graph[output_id] = []
        graph[output_id].append(input_id)
        relation_types[(output_id, input_id)] = rel_type

    # BFS initialization
    queue = deque([(source_id, [])])  # (cur entity, cur path)
    visited = {}  
    visited[source_id] = 1  # mark source entity as visited

    valid_paths = []  # paths to save

    while queue:
        node, path = queue.popleft()

        # check path length
        if len(path) > max_paths:
            continue

        if len(path) > 0 and path[-1][1] == target_id:
            if (
                relation_types.get((path[0][0], path[0][1])) == "transfer" and  # first-hop should be transfer relation
                relation_types.get((path[-1][0], path[-1][1])) == "transfer" and  # last-hop should be transfer relation
                all(relation_types.get((p[0], p[1])) == "invoke" for p in path[1:-1])  # other hops shoule be invoke relation
            ):
                valid_paths.append(path)

                if len(valid_paths) >= max_paths:
                    return valid_paths

        # extend BFS
        for neighbor in graph.get(node, []):
            # allow at most two times for visit
            if visited.get(neighbor, 0) < 3:
                # add neighbourhood to the queue and update the visiting times
                queue.append((neighbor, path + [(node, neighbor)]))
                visited[neighbor] = visited.get(neighbor, 0) + 1  # add visiting times

    return valid_paths

def get_entity_name(entity_id):
    sql = f"""
        SELECT short_name
        FROM schema_entity
        WHERE id = '{entity_id}'
    """
    
    short_name = select_one_from_db(sql)

    return short_name

def get_entity_functionality(entity_id):
    sql = f"""
        SELECT raw_short_name
        FROM schema_entity
        WHERE id = '{entity_id}'
    """
    
    short_name = select_one_from_db(sql)

    return short_name

def get_extend_triples(source_entity_id, target_entity_id):
    sql1 = f"""
    SELECT input_entity_id FROM schema_relationship
    WHERE output_entity_id = '{source_entity_id}' AND relation_type = 'transfer'
    """
    temp_node_list1_result = select_all_from_db(sql1)
    temp_node_list1 = {row[0] for row in temp_node_list1_result}

    sql2 = f"""
    SELECT output_entity_id FROM schema_relationship
    WHERE input_entity_id = '{target_entity_id}' AND relation_type = 'transfer'
    """
    temp_node_list2_result = select_all_from_db(sql2)
    temp_node_list2 = {row[0] for row in temp_node_list2_result}

    intermediate_nodes = list(temp_node_list1 & temp_node_list2)
    new_triples = []
    for node_id in intermediate_nodes:
        new_triples.append(source_entity_id, node_id)
        new_triples.append(node_id, target_entity_id)
        

    return new_triples