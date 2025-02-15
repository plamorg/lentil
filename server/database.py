from chromadb import Collection
import chromadb


class VectorDatabase:
    collection: Collection

    def __init__(self):
        """
        Initialize the database.
        """
        client = chromadb.Client()
        self.collection = client.get_or_create_collection(name="lentil_collection")

    def clear(self):
        """
        Clear the database.
        """
        all_docs = self.collection.get()
        all_ids = all_docs.get("ids")
        if all_ids:
            self.collection.delete(ids=all_ids)

    def add_files(self):
        """
        [("path1", "file_content1"), ...]
        """
        pass
