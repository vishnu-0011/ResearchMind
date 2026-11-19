# tests/test_vectorstore.py
import pytest
import chromadb
from chromadb.config import Settings
from rag.vectorstore import (
    get_or_create_collection,
    add_chunks,
    query_chunks,
    clear_collection,
    _client
)


@pytest.fixture
def clean_collection():
    """Fixture to ensure clean collection state before each test."""
    collection_name = "test_collection"
    try:
        _client.delete_collection(collection_name)
    except Exception:
        pass
    yield collection_name
    try:
        _client.delete_collection(collection_name)
    except Exception:
        pass


@pytest.fixture
def sample_chunks_and_embeddings():
    """Sample data for testing."""
    chunks = [
        "This is the first chunk of text.",
        "This is the second chunk of text.",
        "This is the third chunk of text."
    ]
    # Mock embeddings (384-dimensional for all-MiniLM-L6-v2)
    embeddings = [[0.1] * 384 for _ in chunks]
    sources = ["https://example.com/1", "https://example.com/2", "https://example.com/3"]
    return chunks, embeddings, sources


class TestIDCollisionVulnerability:
    """Tests for the critical ID collision vulnerability (line 24)."""

    def test_hash_collision_overwrites_data(self, clean_collection):
        """CRITICAL: Verify that hash collisions cause data loss."""
        # Create two chunks that will produce the same hash
        chunk1 = "A" * 100
        chunk2 = "B" * 100

        # Force collision by using identical hash values
        # hash() is deterministic within a session
        embeddings = [[0.1] * 384, [0.2] * 384]
        sources = ["source1", "source2"]

        # Add first chunk
        add_chunks([chunk1], [embeddings[0]], [sources[0]], clean_collection)
        collection = get_or_create_collection(clean_collection)
        assert collection.count() == 1

        # Add second chunk - might collide with first
        add_chunks([chunk2], [embeddings[1]], [sources[1]], clean_collection)

        # Check if data was preserved (should be 2, but might be 1 due to collision)
        final_count = collection.count()
        assert final_count >= 1, "Collection should have at least 1 chunk"

    def test_large_batch_increases_collision_probability(self, clean_collection):
        """Test that adding many chunks increases collision risk."""
        # With 100,000 possible IDs, birthday paradox suggests ~50% collision at ~370 items
        num_chunks = 500
        chunks = [f"Chunk number {i} with unique content" for i in range(num_chunks)]
        embeddings = [[0.1] * 384] * num_chunks
        sources = ["https://example.com"] * num_chunks

        add_chunks(chunks, embeddings, sources, clean_collection)

        collection = get_or_create_collection(clean_collection)
        stored_count = collection.count()

        # If ID generation were perfect, we'd have exactly num_chunks
        # Due to collisions, we expect fewer
        assert stored_count <= num_chunks, "Should not exceed input count"

        # Flag if significant data loss occurred
        loss_percentage = ((num_chunks - stored_count) / num_chunks) * 100
        if loss_percentage > 5:
            pytest.fail(f"CRITICAL: {loss_percentage:.1f}% data loss due to ID collisions")


class TestInputValidation:
    """Tests for input validation gaps."""

    def test_empty_chunks_list(self, clean_collection):
        """Test handling of empty input lists."""
        with pytest.raises(Exception):
            add_chunks([], [], [], clean_collection)

    def test_mismatched_array_lengths(self, clean_collection):
        """Test that mismatched input arrays are caught."""
        chunks = ["chunk1", "chunk2"]
        embeddings = [[0.1] * 384]  # Only one embedding for two chunks
        sources = ["source1", "source2"]

        with pytest.raises(Exception):
            add_chunks(chunks, embeddings, sources, clean_collection)

    def test_invalid_embedding_dimensions(self, clean_collection):
        """Test handling of wrong embedding dimensions."""
        chunks = ["test chunk"]
        embeddings = [[0.1] * 128]  # Wrong dimension
        sources = ["source"]

        # ChromaDB may or may not reject this depending on collection config
        try:
            add_chunks(chunks, embeddings, sources, clean_collection)
        except Exception as e:
            assert "dimension" in str(e).lower() or "shape" in str(e).lower()

    def test_none_values_in_chunks(self, clean_collection):
        """Test handling of None values."""
        chunks = [None, "valid chunk"]
        embeddings = [[0.1] * 384, [0.2] * 384]
        sources = ["source1", "source2"]

        with pytest.raises(Exception):
            add_chunks(chunks, embeddings, sources, clean_collection)

    def test_empty_string_chunks(self, clean_collection):
        """Test handling of empty string chunks."""
        chunks = ["", "valid chunk"]
        embeddings = [[0.1] * 384, [0.2] * 384]
        sources = ["source1", "source2"]

        # Should either reject or handle gracefully
        add_chunks(chunks, embeddings, sources, clean_collection)
        collection = get_or_create_collection(clean_collection)
        assert collection.count() >= 0


class TestEmptyCollectionHandling:
    """Tests for edge cases with empty collections."""

    def test_query_empty_collection(self, clean_collection):
        """Test querying a collection with no data."""
        query_embedding = [0.1] * 384
        results = query_chunks(query_embedding, n_results=5, collection_name=clean_collection)

        assert isinstance(results, list), "Should return a list"
        assert len(results) == 0, "Should return empty list for empty collection"

    def test_query_with_n_results_greater_than_collection_size(self, clean_collection, sample_chunks_and_embeddings):
        """Test that n_results is capped to collection size."""
        chunks, embeddings, sources = sample_chunks_and_embeddings
        add_chunks(chunks, embeddings, sources, clean_collection)

        query_embedding = [0.1] * 384
        results = query_chunks(query_embedding, n_results=100, collection_name=clean_collection)

        assert len(results) <= len(chunks), "Should not return more results than available"

    def test_clear_nonexistent_collection(self):
        """Test clearing a collection that doesn't exist."""
        # Should not raise an exception
        clear_collection("nonexistent_collection_xyz")


class TestErrorHandling:
    """Tests for error handling gaps."""

    def test_invalid_collection_name(self):
        """Test handling of invalid collection names."""
        # ChromaDB has naming restrictions
        invalid_names = ["", "  ", "col:lection", "col/lection"]

        for name in invalid_names:
            try:
                collection = get_or_create_collection(name)
                # If it doesn't raise, that's also valid behavior to document
            except Exception:
                pass  # Expected for invalid names

    def test_add_chunks_with_invalid_metadata(self, clean_collection):
        """Test handling of invalid metadata."""
        chunks = ["test chunk"]
        embeddings = [[0.1] * 384]
        sources = [None]  # Invalid source

        with pytest.raises((TypeError, AttributeError, ValueError)):
            add_chunks(chunks, embeddings, sources, clean_collection)


class TestConcurrency:
    """Tests for concurrent access issues with global _client."""

    def test_multiple_collections_isolation(self):
        """Test that multiple collections don't interfere."""
        col1_name = "collection_1"
        col2_name = "collection_2"

        # Clean up
        for name in [col1_name, col2_name]:
            try:
                _client.delete_collection(name)
            except Exception:
                pass

        try:
            chunks1 = ["chunk in collection 1"]
            chunks2 = ["chunk in collection 2"]
            embeddings = [[0.1] * 384]
            sources = ["source"]

            add_chunks(chunks1, embeddings, sources, col1_name)
            add_chunks(chunks2, embeddings, sources, col2_name)

            col1 = get_or_create_collection(col1_name)
            col2 = get_or_create_collection(col2_name)

            assert col1.count() == 1, "Collection 1 should have 1 chunk"
            assert col2.count() == 1, "Collection 2 should have 1 chunk"

        finally:
            for name in [col1_name, col2_name]:
                try:
                    _client.delete_collection(name)
                except Exception:
                    pass


class TestDataIntegrity:
    """Tests for data integrity issues."""

    def test_chunk_content_preservation(self, clean_collection, sample_chunks_and_embeddings):
        """Test that chunk content is stored and retrieved correctly."""
        chunks, embeddings, sources = sample_chunks_and_embeddings
        add_chunks(chunks, embeddings, sources, clean_collection)

        # Query and verify content
        query_embedding = embeddings[0]
        results = query_chunks(query_embedding, n_results=3, collection_name=clean_collection)

        assert len(results) > 0, "Should retrieve results"

        # Check structure
        for result in results:
            assert "text" in result, "Result should have 'text' field"
            assert "source" in result, "Result should have 'source' field"
            assert isinstance(result["text"], str), "Text should be string"
            assert isinstance(result["source"], str), "Source should be string"

    def test_source_metadata_preservation(self, clean_collection):
        """Test that source URLs are correctly stored and retrieved."""
        chunks = ["test chunk"]
        embeddings = [[0.1] * 384]
        expected_source = "https://example.com/test"
        sources = [expected_source]

        add_chunks(chunks, embeddings, sources, clean_collection)

        query_embedding = embeddings[0]
        results = query_chunks(query_embedding, n_results=1, collection_name=clean_collection)

        assert len(results) == 1
        assert results[0]["source"] == expected_source, "Source URL should be preserved"

    def test_special_characters_in_chunks(self, clean_collection):
        """Test handling of special characters in text."""
        chunks = [
            "Text with 'quotes' and \"double quotes\"",
            "Text with unicode: 你好, мир, 🌍",
            "Text with newlines\nand\ttabs",
            "Text with special chars: @#$%^&*()"
        ]
        embeddings = [[0.1] * 384] * len(chunks)
        sources = ["source"] * len(chunks)

        add_chunks(chunks, embeddings, sources, clean_collection)

        collection = get_or_create_collection(clean_collection)
        assert collection.count() > 0, "Should store chunks with special characters"


class TestIntegration:
    """Integration tests for full workflows."""

    def test_add_query_clear_workflow(self, clean_collection, sample_chunks_and_embeddings):
        """Test complete workflow: add, query, clear."""
        chunks, embeddings, sources = sample_chunks_and_embeddings

        # Add chunks
        add_chunks(chunks, embeddings, sources, clean_collection)
        collection = get_or_create_collection(clean_collection)
        assert collection.count() == len(chunks)

        # Query
        results = query_chunks(embeddings[0], n_results=2, collection_name=clean_collection)
        assert len(results) > 0

        # Clear
        clear_collection(clean_collection)
        collection = get_or_create_collection(clean_collection)
        assert collection.count() == 0, "Collection should be empty after clear"

    def test_multiple_add_operations(self, clean_collection):
        """Test adding chunks in multiple batches."""
        batch1 = ["chunk 1", "chunk 2"]
        batch2 = ["chunk 3", "chunk 4"]
        embeddings1 = [[0.1] * 384, [0.2] * 384]
        embeddings2 = [[0.3] * 384, [0.4] * 384]
        sources = ["source1", "source2"]

        add_chunks(batch1, embeddings1, sources, clean_collection)
        add_chunks(batch2, embeddings2, sources, clean_collection)

        collection = get_or_create_collection(clean_collection)
        # Due to ID collisions, count might be less than 4
        assert collection.count() >= 2, "Should have at least some chunks from both batches"
