# GeoGraphRAG

**GeoGraphRAG** is a graph-based Retrieval-Augmented Generation (RAG) approach designed for geospatial modeling, built upon the **S-GMKG** framework.

---

## 📌 Overview

GeoGraphRAG enhances geospatial knowledge representation by leveraging the semantic structure of **S-GMKG**, enabling more accurate and context-aware geospatial reasoning.

---

## 📂 Repository Contents

- **Benchmarks**: Contains 100 sample cases for evaluating performance.
- **`core/` folder**: Stores the core methods of GeoGraphRAG.
- **`core/utils/llm_config.py`**: Defines the basic configuration for LLM usage.
- **`sgmkg.db`**: An instance of the S-GMKG including:
  - `schema_entity` table: 15,224 entities
  - `schema_relation` table: 77,134 relationships

---

## 📖 Reference for S-GMKG

Please refer to the official publication for a detailed introduction to **S-GMKG**:

> **Design and application of a semantic-driven geospatial modeling knowledge graph based on large language models**  
> *Geo-Spatial Information Science*, 2025  
> DOI: [10.1080/10095020.2025.2483884](https://doi.org/10.1080/10095020.2025.2483884)
> ![S-GMKG Architecture](images/S-GMKG%20Structure.png)


---

## 📬 Contact

For questions or collaboration, please contact: **jliang@whu.edu.cn**
