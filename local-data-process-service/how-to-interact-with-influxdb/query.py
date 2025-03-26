from .main import client


query = """SELECT *
FROM 'census'
WHERE time >= now() - interval '24 hours'
AND ('bees' IS NOT NULL OR 'ants' IS NOT NULL)"""

# Execute the query
table = client.query(query=query, database="test-bucket", language='sql')

# Convert to dataframe
df = table.to_pandas().sort_values(by="time")
print(df)