from chromadb import Collection
import chromadb
from typing import List, Tuple, Any


class VectorDatabase:
    collection: Collection

    def __init__(self):
        """
        Initialize the database.
        """
        client = chromadb.PersistentClient()
        self.collection = client.get_or_create_collection(name="lentil_collection")

    def clear(self):
        """
        Clear the database.
        """
        all_docs = self.collection.get()
        all_ids = all_docs.get("ids")
        if all_ids:
            self.collection.delete(ids=all_ids)

    def add_files(self, files: List[Tuple[str, str]]) -> None:
        if not files:
            return

        # Separate out the file paths and contents
        file_paths = [entry[0] for entry in files]
        file_contents = [entry[1] for entry in files]

        # Create metadata dicts (optional but often useful)
        metadatas = [{"path": entry[0]} for entry in files]

        # 1. Check which of these IDs already exist
        existing = self.collection.get(ids=file_paths)
        existing_ids = set(existing.get("ids", []))  # e.g. {"path1", "path2", ...}

        # 2. Delete the overlapping IDs (i.e., paths that already exist)
        if existing_ids:
            self.collection.delete(ids=list(existing_ids))

        # 3. Add all new documents (both brand-new and replacements)
        self.collection.add(
            documents=file_contents,
            metadatas=metadatas,
            ids=file_paths
        )


    def delete_files(self, files: List[Tuple[str, str]]) -> None:
        """
        Deletes a list of documents by their file paths.

        :param files: List of tuples, e.g. [("path1", "file_content1"), ...]
                      Only the first element (path) is used to find and delete.
        """
        if not files:
            return

        file_paths = [entry[0] for entry in files]
        self.collection.delete(ids=file_paths)

    def query(self, query: str, k: int) -> Any:
        """
        Returns the top-k most similar documents for the given query string.
        Flattens the output for a single query to avoid nested lists.
        """
        results = self.collection.query(
            query_texts=[query], n_results=k  # Single query -> shape is 1 x k
        )

        # The default Chroma structure for a single query is nested, e.g.:
        # results["ids"] = [["file1.txt", "file2.txt"]]
        #
        # We want to flatten this to a single list, e.g.:
        # results["ids"] = ["file1.txt", "file2.txt"]

        if results.get("ids"):
            results["ids"] = results["ids"][0]
        if results.get("documents"):
            results["documents"] = results["documents"][0]
        if results.get("metadatas"):
            results["metadatas"] = results["metadatas"][0]
        if results.get("embeddings"):
            results["embeddings"] = results["embeddings"][0]

        return results

