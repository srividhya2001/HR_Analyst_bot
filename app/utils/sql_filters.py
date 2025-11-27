import re


def apply_division_filter(sql: str, division: str) -> str:
    """
    Inject tenant isolation filter into any valid SELECT SQL query.
    Ensures city/filters come before ORDER/GROUP/LIMIT clauses.
    Prevents multiple WHERE clauses.
    """
    division_clause = f"division = '{division}'"
    clean = sql.strip().rstrip(";")

    lower_sql = clean.lower()

    match_where = re.search(r"\bwhere\b", lower_sql)
    match_group = re.search(r"\bgroup\s+by\b", lower_sql)
    match_order = re.search(r"\border\s+by\b", lower_sql)
    match_limit = re.search(r"\blimit\b", lower_sql)

    insert_pos = None

    if match_where:
        insert_pos = match_where.end()
        modified = clean[:insert_pos] + f" {division_clause} AND " + clean[insert_pos:]
        return modified + ";"

    clause_positions = [
        pos for pos in [
            match_group.start() if match_group else None,
            match_order.start() if match_order else None,
            match_limit.start() if match_limit else None,
        ] if pos is not None
    ]

    if clause_positions:
        insert_pos = min(clause_positions)
        modified = (
            clean[:insert_pos]
            + f" WHERE {division_clause} "
            + clean[insert_pos:]
        )
        return modified + ";"

    modified = clean + f" WHERE {division_clause}"
    return modified + ";"