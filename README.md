# GeoGraphRAG

**GeoGraphRAG** is a graph-based Retrieval-Augmented Generation (RAG) approach designed for geospatial modeling, built upon the **S-GMKG** framework. This repository provides:

- Benchmarks for evaluating performance, which include 100 sample cases
- Reference implementations of the approach
- Essential information about the underlying **S-GMKG**

An instance of **S-GMKG** is available in the `sgmkg.db` file, containing two tables: `schema_entity` and `schema_relation`. In total, it includes 15,224 entities and 77,134 relationships.

The `core` folder stores the core methods for GeoGraphRAG (still being actively loaded and updated). Basic configurations for LLM can be found in the `llm_config.py` file within the `utils` directory.

**An official reference for S-GMKG is coming soon—stay tuned for its release!**

By leveraging **S-GMKG**, GeoGraphRAG enhances geospatial knowledge representation, facilitating more accurate and context-aware geospatial reasoning.

For more information, please contact: **jliang@whu.edu.cn**.
