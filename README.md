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
> *Geo-Spatial Information Science*, 2025: 1-20, DOI: [10.1080/10095020.2025.2483884](https://doi.org/10.1080/10095020.2025.2483884)

The following figure illustrates the overall architecture of **S-GMKG**, including the core entity types and relations:

![S-GMKG Architecture](images/S-GMKG%20Structure.png)  

The following table provides a concise reference of the core schema for S-GMKG, focusing on **Functional Step** and **IO-Data** entities, and their associated relations (**Invoke**, **Transfer**). The *Modeling Task* entity and *Contain* relation are omitted here for simplicity.

## 📋 Core Schema of S-GMKG

| Entity / Relation | Attributes / Definition | Notes |
|-------------------|-------------------------|-------|
| **Functional Step** | **StepName**: Name of the functional step | Describes functional module |
|                   | **StepDescr**: Description of functionality | Semantic explanation of operation |
|                   | **inSeries**: List of IO-Data (input) | Input data series |
|                   | **outSeries**: List of IO-Data (output) | Output data series |
|                   | **CodeSnippet**: Code implementation reference {code fragment / API sequence / API list} | May include code fragment, API sequence (e.g., api1 → api2 → api3), or simple API list |
| **IO-Data**       | **DataName**: Short name of data | Semantic identifier of data |
|                   | **DataRole**: {Input, Output, Intermediate} | Data role in modeling flow |
|                   | **Format**: Data format (Remote sensing, Vector, Constant, etc.) | Type of data |
| **Invoke Relation** | **Source → Target**: Functional Step → Functional Step | Execution dependency |
|                   | **frequency**: Integer | Frequency of invocation across modeling processes |
| **Transfer Relation** | **Source ↔ Target**: Functional Step ↔ IO-Data | Data flow connection |
|                   | **connectivity**: Probability ∈ [0,1] | Connection strength (1 within process, <1 across processes) |
|                   | **frequency**: Integer | Co-occurrence frequency in modeling processes |

---

## 📬 Contact

For questions or collaboration, please contact: **jliang@whu.edu.cn**
