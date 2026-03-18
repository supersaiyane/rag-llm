from chunker.text_chunker import chunk_text

text = """
Redis failover procedure involves promoting a replica node
to master and restarting the original master instance.
This ensures high availability.
"""

chunks = chunk_text(text, chunk_size=10, chunk_overlap=2)

for c in chunks:
    print("CHUNK:", c)