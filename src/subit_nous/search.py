"""Hybrid search: SUBIT filter + cosine similarity"""

import json
import sqlite3
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import numpy as np

from .core import text_to_soft, soft_to_hard, subit_to_name, cosine_similarity

DB_PATH = Path.home() / ".subit_nous" / "search.db"

def _get_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY,
            path TEXT UNIQUE,
            soft_b0 REAL, soft_b1 REAL, soft_b2 REAL, soft_b3 REAL,
            soft_b4 REAL, soft_b5 REAL, soft_b6 REAL, soft_b7 REAL,
            mode INTEGER,
            who INTEGER,
            where_axis INTEGER,
            when_axis INTEGER,
            text_preview TEXT
        )
    """)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_mode ON documents(mode)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_who ON documents(who)")
    return conn

def index_folder(folder_path: str, chunk_size: int = 1000) -> int:
    """Індексує всі текстові файли в папці."""
    conn = _get_db()
    cursor = conn.cursor()
    indexed = 0

    text_extensions = {'.txt', '.md', '.py', '.json', '.yaml', '.yml', '.rst', '.csv', '.html', '.css', '.js'}
    files = list(Path(folder_path).rglob("*"))
    for f in files:
        if f.is_file() and f.suffix.lower() in text_extensions:
            try:
                text = f.read_text(encoding='utf-8', errors='ignore')
                if not text.strip():
                    continue
                soft = text_to_soft(text, chunk_size)
                hard = soft_to_hard(soft)
                mode = (hard >> 0) & 0b11
                who = (hard >> 6) & 0b11
                where = (hard >> 4) & 0b11
                when = (hard >> 2) & 0b11
                cursor.execute("""
                    INSERT OR REPLACE INTO documents
                    (path, soft_b0, soft_b1, soft_b2, soft_b3, soft_b4, soft_b5, soft_b6, soft_b7,
                     mode, who, where_axis, when_axis, text_preview)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (str(f), *soft.tolist(), mode, who, where, when, text[:200]))
                indexed += 1
            except Exception as e:
                print(f"Error indexing {f}: {e}")
    conn.commit()
    conn.close()
    return indexed

def search(
    query: str,
    mode: Optional[str] = None,
    who: Optional[str] = None,
    where: Optional[str] = None,
    when: Optional[str] = None,
    top_k: int = 10,
    alpha: float = 0.5,
    chunk_size: int = 1000,
) -> List[Dict]:
    """
    Гібридний пошук.
    alpha: вага семантичної схожості (0..1). 1-alpha – вага SUBIT-фільтра.
    """
    mode_map = {"STATE": 2, "VALUE": 3, "FORM": 1, "FORCE": 0}
    who_map = {"ME": 2, "WE": 3, "YOU": 1, "THEY": 0}
    where_map = {"EAST": 2, "SOUTH": 3, "WEST": 1, "NORTH": 0}
    when_map = {"SPRING": 2, "SUMMER": 3, "AUTUMN": 1, "WINTER": 0}

    query_soft = text_to_soft(query, chunk_size)

    conn = _get_db()
    cursor = conn.cursor()

    sql = "SELECT path, soft_b0, soft_b1, soft_b2, soft_b3, soft_b4, soft_b5, soft_b6, soft_b7, mode, who, where_axis, when_axis FROM documents WHERE 1=1"
    params = []
    if mode is not None:
        sql += " AND mode = ?"
        params.append(mode_map[mode.upper()])
    if who is not None:
        sql += " AND who = ?"
        params.append(who_map[who.upper()])
    if where is not None:
        sql += " AND where_axis = ?"
        params.append(where_map[where.upper()])
    if when is not None:
        sql += " AND when_axis = ?"
        params.append(when_map[when.upper()])

    cursor.execute(sql, params)
    rows = cursor.fetchall()
    conn.close()

    results = []
    for row in rows:
        path, *soft_vals, mode_val, who_val, where_val, when_val = row
        doc_soft = np.array(soft_vals, dtype=np.float32)
        sim = cosine_similarity(query_soft, doc_soft)
        # SUBIT match score (просто 1, якщо пройшов фільтр, інакше 0 – але фільтр вже в SQL)
        subit_score = 1.0
        final_score = alpha * sim + (1 - alpha) * subit_score
        results.append({
            "path": path,
            "score": final_score,
            "similarity": sim,
            "mode": mode_val,
            "who": who_val,
            "where": where_val,
            "when": when_val,
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_k]