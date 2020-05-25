> <a href="https://1bk.github.io/simple-airports-analysis/dbt/docs"><img src="https://1bk.github.io/simple-airports-analysis/docs/img/dbt_logo.png" width="200" alt="dbt_logo" /></a>
>
> ## _**Looking for the &#128073; [dbt documentation website](https://1bk.github.io/simple-airports-analysis/dbt/docs) &#128072; instead?**_

# Simple Airports Analysis - Malaysia  

### Structure
```
M  D  ./models
      ├── base
T [x] │   ├── base_airports
T [x] │   └── base_arrivals__malaysia
      ├── core
T [x] │   ├── fct_airports__malaysia_distances_km
T [x] │   └── fct_arrivals__malaysia_summary
      └── staging
V [ ]     └── stg_airports__malaysia_distances
```
#### Descriptions
Documentation (`D`):
- `[x]` = Documented
- `[ ]` = Not Documented

Materialization (`M`):
- `T` = Table
- `E` = Ephemeral
- `V` = View (non-binding)


### More information

#### Github Repository
- [Simple Airports Analysis]

#### dbt_
- [What is dbt]?
- [Installation]?


[Simple Airports Analysis]:<https://github.com/1bk/simple-airports-analysis/>
[What is dbt]:<https://docs.getdbt.com/docs/overview>
[Installation]:<https://docs.getdbt.com/docs/installation>

