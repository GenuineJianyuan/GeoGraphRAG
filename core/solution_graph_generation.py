#### Solution graph generation
#### Corresponse to Section 3.3(Subgraph self-generation and Solution graph extension)
import json
from utils.chat_with_llm import interact_with_llm
from utils.retrieve_utils import get_entity_name

prompt = '''
    Suppose you are a professional GIS expert. For the modeling task: <{}> A sequence of steps are selected to 
    construct a modeling process as the solution. Please proceed with planning. 

    Given the previous subgraph structure ({}), and a list of candidate steps: [{}], 
    determine the next step to be applied for the modeling task. 
    Response the selected step from the given candidate steps.
    **You must select one of the step from the candidate step**
    Please **Only** reply the info of the selected step exactly in the format as it appears in the list of candidate steps.
'''


with open(r"GeoModelingRAG_DenseGraph.json", "r", encoding = "utf-8") as f:
    sample_results = json.load(f)

## The llm using in this project is set mannually: deepseek-v3, qwen-max, llama-70b, deepseek-r1-distill-qwen-32b, gpt-4o, gpt-3.5-turbo
model_name = "qwen-max"     

## run subgraph retrieval algorithm for each sample
all_solution_graph = {}
item_count = 0
for key, dense_graph_info in sample_results.items():
    is_succeed = False
    try_time = 0
    while try_time<3 and not is_succeed:
        try:
            subgraph = dense_graph_info["triples"]
            ##decide route for each source-target entities pair
            target_entity = dense_graph_info["target"][0]
            record_triple = []  ## record source,target
            record_path = []
            for index, source in enumerate(dense_graph_info["source"]):
                is_source_used = False
                for triple in dense_graph_info["triples"]:
                    if triple[0] == source:
                        is_source_used = True
                        continue
                if not is_source_used:
                    # print(f"{source} is not used in the subgraph")
                    continue
                cur_paths = [source]
                cur_entity_id = source
                llm_response = ""
                count = 0
                while count<=15:  ## prevent infinite loops
                    previous_structure =  " -> ".join(entity for entity in cur_paths)
                    ## generate_candidate_step_info
                    target_set = []
                    for triple in dense_graph_info["triples"]:
                        if triple[0] == cur_entity_id:
                            if triple[1] in target_entity or target_entity in triple[1]:
                                target_set.append(f"{target_entity}")
                            else:
                                candidate_step_name = get_entity_name(triple[1])[:50] if len(get_entity_name(triple[1])) > 50 else get_entity_name(triple[1])
                                target_set.append(f"({triple[1]}){candidate_step_name}")
                    candidate_step_info = ";".join(target_set)
                    modeling_task = dense_graph_info["query"] + "using datasource list in: " +";".join(dense_graph_info["source"]) +"with the output: " + dense_graph_info["target"][0]
                    graph_prompt = prompt.format(modeling_task, previous_structure, candidate_step_info)
                    
                    
                    llm_response = interact_with_llm(graph_prompt)
                    print("llm_response", llm_response, model_name)
                    
                    ## The path finding process ends when the target destination is reached.
                    if target_entity.replace("*","") in llm_response:
                        record_triple.append((cur_entity_id, target_entity))
                        cur_paths.append(target_entity)
                        break
                    else:
                        ## the result of llm_response is like (id)short_name, e.g., (io-data1)entity_name
                        start = llm_response.find("(") + 1  
                        end = llm_response.find(")")       
                        next_step_id = llm_response[start:end]   
                        record_triple.append((cur_entity_id, next_step_id))
                        next_step_name = get_entity_name(next_step_id)
                        cur_paths.append(next_step_name)
                        cur_entity_id = next_step_id
                        count = count + 1
                record_path.append(" -> ".join(cur_paths))

            print(f"{key} Final triples selected: {record_path}")
            all_solution_graph[key] = {}
            all_solution_graph[key]["triples"] = record_triple
            all_solution_graph[key]["path"] = record_path
            is_succeed = True
        except Exception as e:
            print(f"{key} occurs error: {e}, have try {try_time} times")
            try_time += 1
            if try_time >=2:
                record_triple.append((cur_entity_id, target_entity))
                cur_paths.append(target_entity)
                all_solution_graph[key] = {}
                all_solution_graph[key]["triples"] = record_triple
                all_solution_graph[key]["path"] = record_path
                print(f"{key} Final triples selected: {record_path}")
                break    

solution_save_name = f"GeoModelingRAG_Solution_{model_name}.json"            
with open (solution_save_name, "w", encoding="utf-8") as f:
    json.dump(all_solution_graph, f, ensure_ascii=False, indent=4)
# print(len(all_solution_graph))