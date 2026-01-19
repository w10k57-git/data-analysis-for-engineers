import json
from pathlib import Path

import ollama
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams


def get_embedding(text: str) -> list[float]:
    """Generate embedding vector using Ollama."""
    response = ollama.embed(model="nomic-embed-text:latest", input=text)
    return response["embeddings"][0]


def main():
    # Initialize in-memory Qdrant client
    client = QdrantClient(":memory:")
    collection_name = "bearings"

    # Get embedding dimension from a sample text
    sample_embedding = get_embedding("sample text")
    vector_size = len(sample_embedding)

    # CREATE - Create collection
    print("\n=== CREATE Collection ===")
    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
    )
    print(f"Created collection '{collection_name}' with vector size {vector_size}")

    # Load bearing data from JSON file
    data_file = Path(__file__).parent / "bearings_data.json"
    with open(data_file) as f:
        bearings_data = json.load(f)

    # CREATE - Insert bearing records with embeddings
    print("\n=== INSERT Points ===")

    points = []
    for bearing in bearings_data:
        text = f"{bearing['designation']} {bearing['type']} {bearing['description']}"
        vector = get_embedding(text)
        point = PointStruct(
            id=bearing["id"],
            vector=vector,
            payload={
                "designation": bearing["designation"],
                "type": bearing["type"],
                "description": bearing["description"],
            },
        )
        points.append(point)
        print(f"  Added: {bearing['designation']} - {bearing['type']}")

    client.upsert(collection_name=collection_name, points=points)

    # READ - Search for similar bearings
    print("\n=== SEARCH (Read) Operation ===")
    query_text = "bearing for heavy radial loads"
    query_vector = get_embedding(query_text)

    search_results = client.query_points(
        collection_name=collection_name, query=query_vector, limit=3, with_payload=True
    ).points

    print(f"Query: '{query_text}'")
    print("Results:")
    for result in search_results:
        print(f"  ID: {result.id}, Score: {result.score:.4f}")
        print(f"    {result.payload['designation']} - {result.payload['type']}")

    # UPDATE - Modify a bearing's payload
    print("\n=== UPDATE Operation ===")
    updated_bearing = {
        "id": 1,
        "designation": "6205",
        "type": "Deep Groove Ball Bearing",
        "description": "Deep groove ball bearing 6205 with bore 25mm, suitable for high speed and medium radial loads, sealed version available",
    }

    # Generate new embedding for updated description
    updated_text = f"{updated_bearing['designation']} {updated_bearing['type']} {updated_bearing['description']}"
    updated_vector = get_embedding(updated_text)

    client.upsert(
        collection_name=collection_name,
        points=[
            PointStruct(
                id=updated_bearing["id"],
                vector=updated_vector,
                payload={
                    "designation": updated_bearing["designation"],
                    "type": updated_bearing["type"],
                    "description": updated_bearing["description"],
                },
            )
        ],
    )
    print(f"Updated bearing ID {updated_bearing['id']}: {updated_bearing['designation']}")

    # Verify update by searching again
    search_results = client.query_points(
        collection_name=collection_name,
        query=get_embedding("sealed bearing"),
        limit=3,
        with_payload=True,
    ).points
    print("Search for 'sealed bearing' after update:")
    for result in search_results:
        print(f"  ID: {result.id}, Score: {result.score:.4f}")
        print(f"    {result.payload['designation']}: {result.payload['description'][:60]}...")

    # DELETE - Remove a bearing
    print("\n=== DELETE Operation ===")
    delete_id = 3
    client.delete(collection_name=collection_name, points_selector=[delete_id])
    print(f"Deleted bearing with ID {delete_id}")

    # Verify deletion
    all_points = client.scroll(collection_name=collection_name, limit=10)[0]
    print(f"Remaining bearings: {len(all_points)}")
    for point in all_points:
        print(f"  ID: {point.id} - {point.payload['designation']}")


if __name__ == "__main__":
    main()
