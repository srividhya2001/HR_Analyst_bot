import re

ALLOWED_TABLES = {"employee_master_view"}

DISALLOWED_KEYWORDS = [
    "INSERT", "UPDATE", "DELETE", "DROP", "ALTER",
    "TRUNCATE", "COPY", "CREATE", "REPLACE", "MERGE",
    "CALL", "GRANT", "REVOKE"
]


def validate_sql(sql: str) -> tuple:
    """
    Validate LLM-generated SQL for safety and correctness.
    Returns (is_valid: bool, error_message: str).
    """
    if not sql or not sql.strip():
        return False, "SQL is empty."

    clean = sql.strip()

    if clean.count(";") > 1:
        return False, "Multiple statements are not allowed."

    if clean.endswith(";"):
        clean = clean[:-1]

    normalized = clean.upper()

    if not normalized.startswith("SELECT"):
        return False, "Only SELECT statements are allowed."

    for keyword in DISALLOWED_KEYWORDS:
        if keyword in normalized:
            return False, f"Disallowed keyword: {keyword}"

    if not re.search(r"\bLIMIT\s+50\b", normalized):
        return False, "SQL must include LIMIT 50."

    tables = re.findall(r"FROM\s+([a-zA-Z_][a-zA-Z0-9_]*)", normalized)
    for tbl in tables:
        if tbl.lower() not in ALLOWED_TABLES:
            return False, f"Invalid or unknown table: {tbl}"

    return True, ""