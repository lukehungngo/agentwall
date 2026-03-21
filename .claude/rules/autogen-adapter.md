---
paths:
  - "src/agentwall/adapters/autogen.py"
  - "tests/test_autogen_adapter.py"
  - "tests/fixtures/autogen_*/**"
---

# AutoGen Adapter Rules

- Detects `autogen` and `pyautogen` imports.
- Looks for agent constructors: `ConversableAgent`, `AssistantAgent`, `UserProxyAgent`, `GroupChatManager`.
- Detects tool registration via `register_for_llm` / `register_for_execution`, and chat initiation via `initiate_chat`.
- Can use LangChain vector stores — detects same class names.
- All analysis via `ast.parse()`. Never import AutoGen from scanned code.
- Returns a valid `AgentSpec` with empty lists when matched but no patterns found — NOT `None`.
