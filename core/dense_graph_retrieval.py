#### Dense graph retrieval
#### Corresponse to Section 3.3(Dense graph extraction)
import os, json
import itertools
from utils.retrieve_utils import retrieve_path_by_bfs,get_candidate_io_data_entities

all_solution_graph = {}
dir_path = "../benchmark" ## 
unsolved_sample = []

# unsolved_list = ['example114.json']
for file_name in os.listdir(dir_path):
    # if (file_name not in unsolved_list):
    #     continue
    with open(os.path.join(dir_path, file_name), "r", encoding = "utf-8") as f:
        json_content = json.load(f)
    candidate_input_list = json_content["datasource"]
    candidate_output_list = [json_content["output"]]
    input_entity_collection, output_entity_collection = get_candidate_io_data_entities(candidate_input_list,candidate_output_list, 8)
    print(f"{file_name}:")
    
    for index, candidate_input in enumerate(candidate_input_list):
        print(f"[Input] {candidate_input} matches with {input_entity_collection[index]}")
    for index, candidate_output in enumerate(candidate_output_list):
        print(f"[Output] {candidate_output} matches with {output_entity_collection[index]}")

    input_combinations  = list(itertools.product(*input_entity_collection)) ##所有潜在的输入搭配
    solution_set = []
    print(f"[Potential starting and ending entities combination]")
    for combo in input_combinations:
        for output in output_entity_collection[0]:
            solution_set.append({
                "input": list(combo),  
                "output": output
            })
    
    solution_graph = []
    incompleted_solution_graph = []
    ## each solution in the solution set represents a potential modeling solution 
    #  that includes multiple starting and ending nodes(source/targetentities)
    for solution in solution_set:
        is_valid = True
        target_entity_id = solution["output"]
        triple_set = []

        ## Only if there is a path from each current source_entity_id to target_entity_id, 
        # it indicates that the current modeling scheme is reasonable, and is_valid = True
        for source_entity_id in solution["input"]:
            paths = retrieve_path_by_bfs(source_entity_id, target_entity_id)
            if len(paths) == 0:
                is_valid = False
            else:
                for path in paths:
                    triple_set.extend(path)      
        if is_valid:
            source_dict = {}
            for i, input_source in enumerate(solution["input"]):
                source_dict[json_content["datasource"][i]] = input_source
            solution_graph.append({"source":source_dict, "target": {json_content["output"]:solution["output"]}, "triples": triple_set})
        else:
            if len(triple_set)>0:
                source_dict = {}
                for i, input_source in enumerate(solution["input"]):
                    source_dict[json_content["datasource"][i]] = input_source
                incompleted_solution_graph.append({"source":source_dict, "target": {json_content["output"]:solution["output"]},"triples": triple_set})

    if len(solution_graph)>0:
        print(f"Find dense graph for {file_name}: {solution_graph}")
        all_solution_graph[file_name] = {"complete": solution_graph}
    else:
        ## not all paths exist from every source entities to target entity, only a part of them exist.
        if len(incompleted_solution_graph) > 0:
            print(f"Find imcompleted dense graph for {file_name}: {incompleted_solution_graph}") 
            all_solution_graph[file_name] = {"incomplete": incompleted_solution_graph}  
        else:
            unsolved_sample.append(file_name)
            print(f"Cannot find dense graph for {file_name}")     
    print("="*50+'\n')  


# print(unsolved_sample)   
## export the init result as a json file named "GeoModelingRAG.json"
with open(r"GeoModelingRAG.json", "w", encoding="utf-8") as f:
    json.dump(all_solution_graph, f, ensure_ascii=False, indent=4)
    

## get the dense graph for each sample from the  "GeoModelingRAG.json" based on the groups for samples in the json
## for instance, a sample contains two groups: Start->A1->B1->End; Start->A2->B2->End; 
# then the dense graph should include triples for these two groups.

with open(r"GeoModelingRAG.json", "r", encoding="utf-8") as f:
    sample_result = json.load(f)

all_dense_graph = {}
for key, result in sample_result.items():
    if "complete" in result.keys():
        groups = result["complete"]
    else:
        groups = result["incomplete"]
    cur_dense_graph = set()
    for group in groups:
        for triple in group["triples"]:
            if triple[0] in group["source"].values():
                for source_name, entity_id in group["source"].items():
                    if triple[0] == entity_id:
                        cur_dense_graph.add((source_name, triple[1]))
                        continue
            elif triple[1] in group["target"].values():
                for target_name, entity_id in group["target"].items():
                    if triple[1] == entity_id:
                        cur_dense_graph.add((triple[0], target_name))
                        continue
            else:
                cur_dense_graph.add((triple[0], triple[1]))
    all_dense_graph[key] = {"source": list(group["source"].keys()), "target": list(group["target"].keys()), "triples": list(cur_dense_graph)}
    
    ## incorporate "query" from samples in the benchmark
    with open(os.path.join("../benchmark", key), "r", encoding="utf-8") as f:
        cur_sample_info = json.load(f)
    all_dense_graph[key]["query"] = cur_sample_info["query"]

# print(all_dense_graph)

## Construct dense graph for each sample into a json file named "GeoModelingRAG_DenseGraph.json"
with open(r"GeoModelingRAG_DenseGraph.json", "w", encoding="utf-8") as f:
    json.dump(all_dense_graph, f, ensure_ascii=False, indent=4)
