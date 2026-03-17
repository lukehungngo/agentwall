"""Fixture: Unsafe Python config with insecure vector store settings."""

import chromadb

# Ephemeral client — no persistence, no auth
client = chromadb.EphemeralClient()

# Settings with allow_reset
DEBUG = True
ALLOW_RESET = True
