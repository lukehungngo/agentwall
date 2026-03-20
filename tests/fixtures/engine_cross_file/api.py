from auth import get_current_user
from retriever import search_docs


def ask_endpoint(request):
    user_id = get_current_user(request)
    return search_docs(request.body, user_id)
