## Prompt for demand identification, along with an example to demonstrate its usage.
## The response from the LLM follows the format provided in the example.

prompt = '''

Assume you are a GIS expert, and based on the provided demand description,assess the following modeling requirement description based on the clarity of input and output data. Ignore processing steps and methods. Focus solely on whether the input and output are clear and can be directly derived from the requirement description.

Three possible outcomes:

    1. If the requirement is clear and inputs/outputs can be directly derived, please list the input and output objects using keywords or phrases:
    Explicit demand;
    Input Data: [list of specific input data or parameters]
    Output Data: [list of specific output results or objects]

    2. If the requirement is partially clear and some inputs/outputs can be directly derived but there are missing elements, please supplement with potential input/output data based on experience and provide the final answer:
    Semi-explicit demand;
    Input Data: [list of specific input data or parameters]
    Output Data: [list of specific output results or objects]

    3. If the requirement is unclear and it is impossible to directly derive inputs and outputs from the description, please respond with:
    Implicit demand;
    "The requirement is unclear. Please provide a more precise description."


Notes: 
    1. **Input Data refers to specific imagery or datasets**. It should not be abstract values or results that need further processing to be identified. Only concrete datasets or parameters are considered clear inputs.
    2. **Do not infer or add anything beyond the original description**. If the description does not include clear inputs and outputs, it is deemed unclear.
    3. Point out the type of output, chose one of:  Vector, Raster, Remote Sensing, Text, Numerical, Unknown
    
Few-shot Examples:
    1. [Demand Description]:Please use Landsat imagery to obtain the land use/cover map for Wuhan city in 2024.
       [Answer] Explicit demand; Input Data: Landsat imagery (Remote Sensing); Output Data: Land use/cover category map(Raster);
       [Reason] This requirement is clear, and both inputs and outputs can be easily identified from the description.

    2. [Demand Description]:Please assess the water area change in Poyang Lake between winter and summer.
       [Answer] Semi-explicit demand; Input Data: Poyang Lake imagery data (winter and summer imagery) (Unknown); Output Data: Water change area (Raster);
       [Reason] The requirement is fairly clear but lacks explicit information on the type of imagery. Thus, we make a reasonable assumption to complete the missing part.

    3. [Demand Description]:Please assess the crop growth status in Hubei province during the fall of 2024.
       [Answer] Implicit demand; The demand description is unclear, please provide a more precise description.
       [Reason] This description is vague. It lacks specific input data (such as the type of imagery) and how the crop growth status is quantified.

Current Demand Description:
    {}
    
Please analysis current demand description and reply in the format exactly as the example.
'''
from utils.chat_with_llm import interact_with_llm

## An instance tha shows the demand identification using example in the benchmark
demand_description_instance = '''Please generate a landslide susceptibility map for Xunwu County in 2024.I have Landsat 8 
                                 images, DEM, ROl, and land use/coverimage for this region as datasource.'''

response = interact_with_llm(demand_description_instance, "gpt-4o")

