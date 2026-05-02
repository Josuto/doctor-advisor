import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict


class QueryMemory:
    """Manages in-memory and persistent storage of patient queries."""

    def __init__(self, memory_file: Path):
        self.memory_file = memory_file
        self.queries: List[Dict] = []
        self._load_recent_from_file()

    def _load_recent_from_file(self) -> None:
        """Load queries from the last 7 days from JSON file into memory."""
        if not self.memory_file.exists():
            return

        try:
            with open(self.memory_file, 'r', encoding='utf-8') as f:
                all_queries = json.load(f)
        except (json.JSONDecodeError, IOError):
            return

        cutoff_date = datetime.now() - timedelta(days=7)
        self.queries = [
            query for query in all_queries
            if datetime.fromisoformat(query['timestamp']) > cutoff_date
        ]

    def add_query(self, query: str) -> None:
        """Add a new query to in-memory storage and persist to file."""
        memory_entry = {
            'query': query,
            'timestamp': datetime.now().isoformat()
        }
        self.queries.append(memory_entry)
        self._save_to_file()

    def get_recent_queries(self) -> List[str]:
        """Return formatted list of recent queries (last 7 days)."""
        cutoff_date = datetime.now() - timedelta(days=7)
        recent = [
            query for query in self.queries
            if datetime.fromisoformat(query['timestamp']) > cutoff_date
        ]

        if not recent:
            return []

        formatted = []
        for query in recent:
            timestamp = datetime.fromisoformat(query['timestamp']).strftime('%Y-%m-%d %H:%M')
            formatted.append(f"[{timestamp}] {query['query']}")

        return formatted

    def _save_to_file(self) -> None:
        """Save all queries (in-memory) to JSON file."""
        self.memory_file.parent.mkdir(parents=True, exist_ok=True)

        # Load all existing queries from file to preserve older entries
        all_queries = []
        if self.memory_file.exists():
            try:
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    all_queries = json.load(f)
            except (json.JSONDecodeError, IOError):
                all_queries = []

        # Merge with in-memory queries (in-memory takes precedence for duplicates)
        existing_timestamps = {q['timestamp'] for q in self.queries}
        for query in all_queries:
            if query['timestamp'] not in existing_timestamps:
                self.queries.append(query)

        # Write all queries back to file
        with open(self.memory_file, 'w', encoding='utf-8') as f:
            json.dump(self.queries, f, indent=2)
