"""
Interactive SQL Query Runner for Amazon Brazil E-Commerce Analysis
Powered by DuckDB
"""
import duckdb
import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

con = duckdb.connect('ecommerce.duckdb')

print("="*70)
print(" Amazon Brazil E-Commerce SQL Analysis (DuckDB)")
print("="*70)
print("Type your SQL query below (or type 'exit' / 'quit' to close).")
print("Tip: To view available tables, type: SHOW TABLES;")
print("="*70)

while True:
    try:
        query = input("\nSQL> ").strip()
        if not query:
            continue
        if query.lower() in ('exit', 'quit', 'q'):
            print("Exiting...")
            break
        
        # Remove trailing semicolon if present
        if query.endswith(';'):
            query = query[:-1]
            
        df = con.execute(query).df()
        if df.empty:
            print("(No rows returned)")
        else:
            print(df.to_string(index=False))
            print(f"\n({len(df)} rows returned)")
    except KeyboardInterrupt:
        print("\nExiting...")
        break
    except Exception as e:
        print(f"Error: {e}")

con.close()
