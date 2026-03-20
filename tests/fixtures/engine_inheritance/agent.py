from langchain_community.vectorstores import Chroma


class TenantChroma(Chroma):
    def similarity_search(self, query, **kwargs):
        kwargs["filter"] = {"user_id": self.current_user}
        return super().similarity_search(query, **kwargs)


db = TenantChroma(collection_name="docs")
results = db.similarity_search("query")
