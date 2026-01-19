"""
Simple DuckDB with Pandas Demo - Bearing Database
Demonstrates how DuckDB works seamlessly with Pandas DataFrames for analytical queries.
"""

from pathlib import Path

import duckdb
import pandas as pd

data_file = Path(__file__).parent / "bearings_data.json"


def main():
    # Connect to in-memory DuckDB database
    con = duckdb.connect(":memory:")

    # Load bearing data from JSON into Pandas DataFrame
    print("\n=== Load Data into Pandas DataFrame ===")
    df = pd.read_json(data_file)
    print(f"Loaded {len(df)} bearings into DataFrame")
    print(df)

    # CREATE - Register DataFrame with DuckDB (no need to create table manually!)
    print("\n=== Query Pandas DataFrame with DuckDB SQL ===")
    # DuckDB can query Pandas DataFrames directly using SQL
    result_df = con.execute("SELECT * FROM df").df()
    print("All bearings (queried via DuckDB SQL):")
    print(result_df)

    # READ - Analytical queries on DataFrame using SQL
    print("\n=== Analytical Queries ===")

    # Query 1: Filter bearings with bore diameter >= 25mm
    query1 = """
        SELECT designation, bearing_type, bore_diameter
        FROM df
        WHERE bore_diameter >= 25.0
        ORDER BY bore_diameter DESC
    """
    result_df = con.execute(query1).df()
    print("\nBearings with bore diameter >= 25mm:")
    print(result_df)

    # Query 2: Aggregate statistics by bearing type
    query2 = """
        SELECT
            bearing_type,
            COUNT(*) as count,
            AVG(load_rating) as avg_load_rating,
            MAX(bore_diameter) as max_bore_diameter
        FROM df
        GROUP BY bearing_type
    """
    result_df = con.execute(query2).df()
    print("\nStatistics by bearing type:")
    print(result_df)

    # Query 3: Complex filtering and calculations
    query3 = """
        SELECT
            designation,
            bearing_type,
            bore_diameter,
            outer_diameter,
            (outer_diameter - bore_diameter) as wall_thickness,
            load_rating,
            ROUND(load_rating / bore_diameter, 2) as load_per_mm_bore
        FROM df
        WHERE load_rating > 15.0
        ORDER BY load_per_mm_bore DESC
    """
    result_df = con.execute(query3).df()
    print("\nBearings with load rating > 15 kN (with calculated metrics):")
    print(result_df)

    # UPDATE - Create modified DataFrame
    print("\n=== Update Data ===")
    # In analytical workflows, we typically create new DataFrames rather than updating in-place
    updated_df = con.execute("""
        SELECT
            designation,
            bearing_type,
            bore_diameter,
            outer_diameter,
            width,
            CASE
                WHEN designation = '6205' THEN 15.3
                ELSE load_rating
            END as load_rating
        FROM df
    """).df()
    print("Updated load rating for bearing 6205:")
    print(updated_df[updated_df["designation"] == "6205"])

    # DELETE - Filter out rows (analytical style)
    print("\n=== Filter Data ===")
    filtered_df = con.execute("""
        SELECT * FROM df
        WHERE designation != '51105'
    """).df()
    print(f"\nDataFrame after filtering out '51105': {len(filtered_df)} bearings")
    print(filtered_df)

    # BONUS: Using DuckDB's relational API with Pandas
    print("\n=== DuckDB Relational API ===")
    rel = con.from_df(df)
    result_df = (
        rel.filter("bore_diameter >= 25.0")
        .project("designation, bearing_type, bore_diameter, load_rating")
        .order("load_rating DESC")
        .df()
    )
    print("Using relational API (filter, project, order):")
    print(result_df)

    # Close connection
    con.close()


if __name__ == "__main__":
    main()
