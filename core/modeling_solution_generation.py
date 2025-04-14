#### Textual Modeling Solution Generation & Code Implenetation
#### Corresponse to Section 3.4
#### Still Under Updating...

import json
from utils.chat_with_llm import interact_with_llm
import pandas as pd
from utils.retrieve_utils import get_extend_triples, get_entity_name, get_entity_functionality
import os,json

prompt_modeling_solution = '''
    Suppose you are a professional GIS expert. Given a geospatial modeling task: {}

    You are asked to implement this task in natural language according to using my solution graph as reference that contains a list of processing steps connected with "->"

    The solution graph for this model is described as follow:
    ``` path
    {}

    ```
    {}

    Please generate a detailed modeling plan following the instructions below and do not forget them:
    (1) Think step by step;
    (2) You have to first consider and describe a modeling solution in natural language to solve this task.
    (3) Compare the generated modeling solution and the given plan, judge the necessary processing steps in the given path that 
        is useful to suppliment your modeling solution. You **must select several processing steps from the plan**  
        Please give you decision to each processing step in the path, and answer which steps do you reserve.
    (4) Remove unnecessary processing step if you decide it is unnecessary;
        -- so please answer if you will remove any processing step?
    (5) Describe your final modeling solution using a list of steps (less than 10 steps), each step is described in less than 50;
    (6) Following the referenced path and the generated solution, determine and describe the connection between selected steps. 
    (7) Your have to reply **exactly** in the format as follow (Do not miss the ```solution and ``` in your reply):
    ``` response
       (your resopnse to the given instructions to think, and answer the question in (2)(3)(4)(5)(6))
    ```
    ```solution
       [1]Description to step 1;
       [2]Description to step 2;
       [3]Description to step 3;
       [4]Description to step 4;
        ...More steps...
    ```
'''

prompt_entity_relations = '''
    [Step {}]. The Functional Step ({}) can be used to for ({}) using iodata ({})
    and produce output [{}]. Here is a implementation code to develop this function: 
    <CodeSnippet:{}>
'''


def get_step_context_info(triples):
    extend_triples = triples

    for pair in triples:
        if not (("step_" in pair[0]) and ("step_" in pair[1])):
            continue
        new_triples = get_extend_triples(pair[0], pair[1])
        extend_triples.extend(new_triples) ## new extended subgraph with transfer relations.
    
    prompt_entity_relations_list = []
    index = 0
    for pair in extend_triples:
        if (("step_" in pair[0]) and ("step_" in pair[1])):  ## only procceed triples with transfer relations
            continue
        
        if (("step_" in pair[0]) and  ("step_" not in pair[1])): ## (step_xxx, iodata_xxx)
            cur_step_name = get_entity_name(pair[0])
            cur_step_func = get_entity_functionality(pair[0])
            ## find input data node for current entities
            cur_input_entities_names = []
            for temp_pair in extend_triples:
                if ("step_" not in temp_pair[0]) and (temp_pair[1] == pair[0]):
                    cur_input_entities_names.append(get_entity_name(temp_pair[0]))
            prompt_entity_relations_list.append(prompt_entity_relations.format(index, cur_step_name, cur_step_func, str(cur_input_entities_names), pair[1], None)) ## code_snippet is not provided in this version
        if (("step_" not in pair[0]) and  ("step_" in pair[1])): ## (iodata_xxx, step_xxx)
            cur_step_name = get_entity_name(pair[1])
            cur_step_func = get_entity_functionality(pair[1])
            ## find output data node for current entities
            cur_output_entities_names = []
            for temp_pair in extend_triples:
                if  (pair[1]==temp_pair[0]) and  ("step_" not in temp_pair[1]):
                    cur_output_entities_names.append(get_entity_name(temp_pair[1]))
            prompt_entity_relations_list.append(prompt_entity_relations.format(index, cur_step_name, cur_step_func, pair[0], str(cur_output_entities_names), None)) ## code_snippet is not provided in this version        
        
        index = index + 1
        
    return prompt_entity_relations_list
        
        
## for modeling solution generation
with open(r"GeoModelingRAG_DenseGraph.json", "r", encoding= "utf-8") as f:
    results = json.load(f)
    
baseline_list = ["GeoModelingRAG_Solution_qwen.json","GeoModelingRAG_Solution_ds_v3.json",
                 "GeoModelingRAG_Solution_ds_r1_32.json", "GeoModelingRAG_Solution_llama70.json",
                 "GeoModelingRAG_Solution_gpt4.json", "GeoModelingRAG_Solution_gpt3_5.json"]

for baseline in baseline_list:
    with open(baseline, "r", encoding= "utf-8") as f:
        solutions = json.load(f)
    modeling_solution_list = []
    for key, solution in solutions.items():
        user_demand = results[key]["query"] + "using datasources "+ ";".join(f"{i+1}. {item}" for i, item in enumerate(results[key]["source"])) +"and produce output:" + results[key]["target"][0]
        cur_plan = ";".join(f"{i+1}. {item}" for i, item in enumerate(solution["path"]))
        
        ## Note, prompt_entity_relations_list coresponses to "Solution graph extension", which is an optional extension 
        
        
        ##
        triples = get_step_context_info(solution["triples"])
        step_context_info  = get_step_context_info(triples)
            
                
        
        is_succeed = False
        while not is_succeed:
            try:
                prompt = prompt_modeling_solution.format(user_demand, cur_plan, step_context_info)
                content = interact_with_llm(prompt) ## deepseek-v3
                modeling_solution = content.split("```solution")[1].split("```")[0]
                is_succeed = True
                cur_index = len(modeling_solution_list) + 1
                modeling_solution_list.append({"Sample": key, "Solution": modeling_solution})
                print(f"{cur_index}-Finish generate modeling solution for {key} in {baseline}")
            except Exception as e:
                print(e)
    
    ## save the textual modeling solution into the csv file
    csv_name = baseline.split('.')[0]
    df = pd.DataFrame(modeling_solution_list)
    csv_file_name = f'{csv_name}.csv'
    df.to_csv(csv_file_name, index=False)
    print(f"CSV saved: '{csv_file_name}'") 


prompt_code = '''
    Suppose you are a professional GISer, given a geospatial modeling task <{}>;
    Here is a modeling solution to help implement this model:
    
        {};
        
    Please follow the instructions below:
    (1) **Think step by step** to develop code snippets for each processing step in the modeling solution;
    (2) Develop code in <Environment: {}> using <Programming Language: {}>
    (3) Generate the implementation program by integrating code snippets developed in (1);
    (4) ** Do not lose** any specific development for the processing step;
    (5) Reply with the final implementation code in the format exactly as follow:
    
    ```javascript
    (the entire assembly program)
    ```
'''    


# for impelemtation code generation

# root_save_dir_path = r"Absolute Path"

# save_dir_path = os.path.join(root_save_dir_path, "GeoModelingRAG")
# if not os.path.isdir(save_dir_path):
#     os.makedirs(save_dir_path)

# # csv results from the above codes for modeling solution generation
# solution_path_list = [
#                  r"D:\Work\Data\GSN_Projects\GRAG\evaluation\GeoModelingRAG\GeoModelingRAG_Solution_qwen.csv",
#                  r"D:\Work\Data\GSN_Projects\GRAG\evaluation\GeoModelingRAG\GeoModelingRAG_Solution_ds_v3.csv",
#                  r"D:\Work\Data\GSN_Projects\GRAG\evaluation\GeoModelingRAG\GeoModelingRAG_Solution_llama70.csv",
#                  r"D:\Work\Data\GSN_Projects\GRAG\evaluation\GeoModelingRAG\GeoModelingRAG_Solution_ds_r1_32.csv",
#                  r"D:\Work\Data\GSN_Projects\GRAG\evaluation\GeoModelingRAG\GeoModelingRAG_Solution_gpt4.csv",
#                  r"D:\Work\Data\GSN_Projects\GRAG\evaluation\GeoModelingRAG\GeoModelingRAG_Solution_gpt3_5.csv",
#                  ]


# for index, solution_path in enumerate(solution_path_list):
#     csv_name = solution_path.split('\\')[-1].split('.')[0]  # 提取文件名并去掉扩展名
#     csv_file_name = os.path.join(save_dir_path, f'{csv_name}.csv')
    
#     solution_df = pd.read_csv(solution_path)
    
#     for j, row in solution_df.iterrows():
#         sample_name = row['Sample']
#         solution = row['Solution']
#         with open(os.path.join("../benchmark", sample_name), "r", encoding = 'utf-8') as f:
#             sample = json.load(f)
#         user_demand = sample["query"] + "using datasources "+ ";".join(f"{i+1}. {item}" for i, item in enumerate(sample["datasource"])) +"and produce output:" + sample["output"]
#         cur_prompt = prompt.format(user_demand, solution, "Google Earth Engine", "JavaScript")
        
#         is_succeed = False
#         while not is_succeed:
#             try:
#                 content = interact_with_llm(cur_prompt)
#                 content1 = content.split("```javascript")[1].split("```")[0]
#                 is_succeed = True
                
#             except Exception as e:
#                 print(e)
        
#         new_row = {"Sample": sample_name, "CodeImpl": content1,"entire": content}
#         df = pd.DataFrame([new_row])
        
#         # 检查文件是否存在，如果存在则追加，否则创建新文件
#         if os.path.exists(csv_file_name):
#             df.to_csv(csv_file_name, mode='a', header=False, index=False)
#         else:
#             df.to_csv(csv_file_name, index=False)
#         print(f"{j}/100: {new_row} written to {csv_file_name}")