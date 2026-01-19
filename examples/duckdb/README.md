# DuckDB with Pandas Examples

This directory contains examples demonstrating how to use DuckDB with Pandas DataFrames for analytical queries.

## Prerequisites

To run these examples, you need to have:

**Python packages**:

```bash
pip install duckdb pandas
```

## Running the Examples

```bash
python duckdb_example.py
```

This example demonstrates how DuckDB seamlessly integrates with Pandas DataFrames, allowing you to:

- Query Pandas DataFrames using SQL
- Perform complex analytical queries and aggregations
- Use both SQL syntax and DuckDB's relational API
- Create derived DataFrames with transformations

## About DuckDB

DuckDB is an in-process SQL OLAP database management system designed for fast analytical queries. It excels at:

- **Pandas Integration**: Query DataFrames directly without loading data into tables
- **Performance**: Faster than Pandas for complex aggregations and joins
- **SQL Power**: Use full SQL capabilities on your DataFrame data
- **Zero-Copy**: Works directly with Pandas data in memory, no data copying needed

## Why Use DuckDB with Pandas?

DuckDB is ideal for analytical workflows where you want SQL's power and performance while working with Pandas. It's particularly useful for:

- Complex GROUP BY and aggregation queries
- Multi-table joins
- Window functions and advanced analytics
- Processing larger-than-memory datasets efficiently
