{% docs __overview__ %}

# Simple Airports Analysis - Malaysia 

### Github Repository
- [Simple Airports Analysis]

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

#### dbt_
- [What is dbt]?
- [Installation]?

[Simple Airports Analysis]:<https://github.com/1bk/simple-airports-analysis/>
[What is dbt]:<https://docs.getdbt.com/docs/overview>
[Installation]:<https://docs.getdbt.com/docs/installation>

{% enddocs %}