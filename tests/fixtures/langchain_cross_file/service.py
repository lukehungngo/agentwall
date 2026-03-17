"""Fixture: Cross-file caller — calls retriever.do_search()."""
from retriever import do_search


def handle_request(user_id, query):
    """Handle a user request — calls do_search without passing user_id."""
    results = do_search(query)
    return results
