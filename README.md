# GeoGraphRAG

**GeoGraphRAG** is a graph-based Retrieval-Augmented Generation (RAG) approach designed for geospatial modeling, built upon the **S-GMKG** framework. This repository provides:

- Benchmarks for evaluating performance, which include 100 sample cases
- Reference implementations of the approach
- Essential information about the underlying **S-GMKG**

An instance of **S-GMKG** is available in the `sgmkg.db` file, containing two tables: `schema_entity` and `schema_relation`. In total, it includes 15,224 entities and 77,134 relationships.

The `core` folder stores the core methods for GeoGraphRAG (still being actively loaded and updated). Basic configurations for LLM can be found in the `llm_config.py` file within the `utils` directory.

For more details about **S-GMKG**, please refer to the official publication:  
**[Design and application of a semantic-driven geospatial modeling knowledge graph based on large language models](https://www.tandfonline.com/doi/full/10.1080/10095020.2025.2483884#d1e2516)**, *Geo-Spatial Information Science*, 2025.

By leveraging **S-GMKG**, GeoGraphRAG enhances geospatial knowledge representation, facilitating more accurate and context-aware geospatial reasoning.

For more information, please contact: **jliang@whu.edu.cn**.
