FORBIDDEN_KEYWORDS = [
    "drop",
    "delete",
    "truncate",
    "alter",
    "update",
    "insert",
    "create",
    "replace"
]

def is_safe_sql(sql: str) -> bool:
    """
    Ensures LLM-generated SQL is READ-ONLY.
    Returns True only if query is safe.
    """

    if not sql:
        return False

    sql_lower = sql.lower().strip()

    # Must start with SELECT
    if not sql_lower.startswith("select"):
        return False

    # Block dangerous keywords
    for keyword in FORBIDDEN_KEYWORDS:
        if keyword in sql_lower:
            return False

    return True
