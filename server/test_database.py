import pytest
from typing import List, Tuple
from database import VectorDatabase  # <-- Import your class from its module


@pytest.fixture
def db() -> VectorDatabase:
    """
    Pytest fixture to create and return a fresh VectorDatabase instance.
    Before each test, we clear the collection to ensure a clean state.
    """
    database = VectorDatabase()
    database.clear()
    return database

def test_sanity():
    assert True

def test_initial_clear(db: VectorDatabase):
    """
    Test that the database is initially cleared.
    """
    all_docs = db.collection.get()
    assert len(all_docs.get("ids", [])) == 0, "Database should be empty after clear."


def test_add_files(db: VectorDatabase):
    """
    Test that add_files successfully inserts documents.
    """
    files_to_add = [
        ("main.c", "int main() { return 0; }"),
        ("utils.c", "void helper() {}")
    ]

    db.add_files(files_to_add)
    all_docs = db.collection.get()

    # Check that the docs are indeed in the collection
    # 'all_docs' typically has keys: 'ids', 'embeddings', 'documents', 'metadatas'
    ids = all_docs.get("ids", [])
    documents = all_docs.get("documents", [])
    metadatas = all_docs.get("metadatas", [])

    assert len(ids) == 2, "There should be 2 document IDs in the collection."
    assert "main.c" in ids and "utils.c" in ids, "The IDs should match the file paths."
    assert len(documents) == 2, "There should be 2 documents in the collection."
    assert len(metadatas) == 2, "There should be 2 metadata entries in the collection."

    # Check content just to be sure
    main_index = ids.index("main.c")
    assert documents[main_index] == "int main() { return 0; }", "Document content should match."
    assert metadatas[main_index]["path"] == "main.c", "Metadata path should match 'main.c'."


def test_query(db: VectorDatabase):
    """
    Test the query method returns the top-k most similar documents.
    NOTE: If you don't have a real embedding function, results may be random/fake.
    """
    files_to_add = [
        ("file1.txt", "This is some text about Python."),
        ("file2.txt", "Here we discuss Python and data science."),
        ("file3.txt", "Unrelated content about cooking recipes.")
    ]
    db.add_files(files_to_add)

    # Query for documents related to 'Python'
    query_result = db.query("Python", k=2)

    # 'query_result' is typically a dict with keys:
    #  'ids', 'metadatas', 'documents', 'embeddings'
    # The default/fake embedding might not rank them strictly by relevance,
    # but we can at least check that we got 2 results back.
    assert len(query_result.get("ids", [])) == 2, "Should return top-2 results."

    # If you have a real embedding model, you might assert that the two
    # documents referencing 'Python' are the top results.
    # For now, just check that the method returns *something*.
    assert "file1.txt" in query_result["ids"] or "file2.txt" in query_result["ids"], (
        "One of the Python-related files should be in the top-2."
    )


def test_delete_files(db: VectorDatabase):
    """
    Test the delete_files method to ensure documents are removed.
    """
    files_to_add = [
        ("main.c", "int main() { return 0; }"),
        ("utils.c", "void helper() {}")
    ]
    db.add_files(files_to_add)

    # Delete just main.c
    db.delete_files([("main.c", "int main() { return 0; }")])

    all_docs = db.collection.get()
    ids_after_delete = all_docs.get("ids", [])

    assert "main.c" not in ids_after_delete, "main.c should have been removed."
    assert "utils.c" in ids_after_delete, "utils.c should still be present."


def test_clear(db: VectorDatabase):
    """
    Test the clear method to ensure all documents are removed.
    """
    files_to_add = [
        ("test1.txt", "Test content 1"),
        ("test2.txt", "Test content 2")
    ]
    db.add_files(files_to_add)

    # Verify they're in the collection
    all_docs_before = db.collection.get()
    assert len(all_docs_before.get("ids", [])) == 2, "Should have 2 docs initially."

    db.clear()
    all_docs_after = db.collection.get()
    assert len(all_docs_after.get("ids", [])) == 0, "All docs should be removed after clear."

def test_replace_existing_document(db: VectorDatabase):
    """
    Test that if a file already exists in the collection, re-adding it replaces 
    the old content but keeps the same ID/path.
    """
    # 1. Add an initial file
    initial_files = [("config.yaml", "version: 1.0\n")]
    db.add_files(initial_files)

    # 2. Add a 'replacement' content for the same path
    updated_files = [("config.yaml", "version: 2.0\n")]
    db.add_files(updated_files)

    # 3. Fetch all docs and verify there's only 1 ID and its content is updated
    all_docs = db.collection.get()
    ids = all_docs.get("ids", [])
    documents = all_docs.get("documents", [])

    assert len(ids) == 1, "There should be only 1 document ID after upsert."
    assert "config.yaml" in ids, "The existing ID/path should remain the same."

    # Check that the content is the 'updated' one
    config_index = ids.index("config.yaml")
    assert documents[config_index] == "version: 2.0\n", "Document content should be replaced."


def test_add_files_empty_list(db: VectorDatabase):
    """
    Test that adding an empty list of files does not cause errors or change the DB.
    """
    # 1. Ensure DB is empty
    all_docs_before = db.collection.get()
    assert len(all_docs_before.get("ids", [])) == 0, "DB should be empty initially."

    # 2. Try adding an empty list
    db.add_files([])

    # 3. Confirm DB is still empty
    all_docs_after = db.collection.get()
    assert len(all_docs_after.get("ids", [])) == 0, "DB should remain empty after adding no files."


def test_idempotent_add(db: VectorDatabase):
    """
    Test that repeatedly adding the same files doesn't create duplicate entries.
    With upsert logic, adding the same path multiple times should keep one doc.
    """
    files_to_add = [
        ("main.c", "int main() { return 0; }"),
        ("utils.c", "void helper() {}")
    ]

    # 1. Add the files once
    db.add_files(files_to_add)

    # 2. Add the same files again (no content changes)
    db.add_files(files_to_add)

    # 3. Fetch all docs and verify we have only 2 IDs total (no duplicates)
    all_docs = db.collection.get()
    ids = all_docs.get("ids", [])
    documents = all_docs.get("documents", [])

    assert len(ids) == 2, "Adding the same files twice should not create duplicates."
    assert "main.c" in ids and "utils.c" in ids, "File paths should still be the same."

    # 4. Optionally confirm content hasn't changed
    main_index = ids.index("main.c")
    utils_index = ids.index("utils.c")
    assert documents[main_index] == "int main() { return 0; }"
    assert documents[utils_index] == "void helper() {}"


def test_partial_upsert(db: VectorDatabase):
    """
    Test that if you add multiple files, then re-add one of them with new content,
    only that file is replaced while the other remains unchanged.
    """
    files_initial = [
        ("file1.txt", "Initial content 1"),
        ("file2.txt", "Initial content 2"),
    ]
    db.add_files(files_initial)

    # Re-add file1 with updated content, leave file2 unchanged
    files_updated = [
        ("file1.txt", "Updated content 1"),
    ]
    db.add_files(files_updated)

    all_docs = db.collection.get()
    ids = all_docs.get("ids", [])
    docs = all_docs.get("documents", [])

    # We should still have exactly 2 IDs
    assert len(ids) == 2, "Should still have 2 documents total."

    # file1.txt should now have updated content
    file1_index = ids.index("file1.txt")
    assert docs[file1_index] == "Updated content 1", "file1.txt should be replaced with new content."

    # file2.txt should remain as is
    file2_index = ids.index("file2.txt")
    assert docs[file2_index] == "Initial content 2", "file2.txt should remain unchanged."
