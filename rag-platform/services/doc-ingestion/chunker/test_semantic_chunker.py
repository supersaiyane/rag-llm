from chunker.semantic_chunker import semantic_chunk_text

text = """
Redis failover happens when the master fails.
A replica is promoted to master.

Replication keeps Redis nodes synchronized.

Recovery involves restarting the failed master.
"""

chunks = semantic_chunk_text(text, max_chunk_size=100)

for c in chunks:
    print("\nCHUNK:")
    print(c)