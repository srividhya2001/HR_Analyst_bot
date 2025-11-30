from app.llm.sql_generator import generate_sql_query
from app.llm.summarizer import summarize_results
from app.db.session import run_query
from app.services.sql_validator import validate_sql
from app.utils.sql_filters import apply_division_filter
from app.core.logging import get_logger

logger = get_logger("service.chat")


def process_query(user_id: str, user_division: str, question: str):
    """
    Orchestrate SQL generation, validation, tenant filtering, execution, and summarization.
    """
    logger.info(
        "Processing query user_id=%s division=%s",
        user_id,
        user_division,
    )

    sql = generate_sql_query(question)
    logger.info("Generated SQL: %s", sql)

    is_valid, error_msg = validate_sql(sql)
    if not is_valid:
        logger.warning(
            "SQL validation failed for user_id=%s: %s",
            user_id,
            error_msg,
        )
        raise Exception(f"SQL validation failed: {error_msg}")

    sql_filtered = apply_division_filter(sql, user_division)
    logger.info("Tenant-filtered SQL: %s", sql_filtered)

    df = run_query(sql_filtered,division=user_division)
    records = df.to_dict(orient="records")

    answer = summarize_results(question, df)

    logger.info(
        "Query successful user_id=%s rows=%d",
        user_id,
        len(records),
    )

    return answer, sql_filtered, records
