from openai import OpenAI
from app.core.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)


def summarize_results(question: str, df):
    """
    Generate a concise natural-language summary of query results.
    """
    preview = df.head(10).to_string(index=False)

    prompt = (
        "You are an analytics summarizer. Produce a brief 2-4 line summary of the data. "
        "Do not mention SQL. Do not hallucinate. Base the summary strictly on the data. "
        f"Question: {question}\n"
        f"Data:\n{preview}"
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        messages=[
            {"role": "system", "content": "Provide factual, concise analytical summaries."},
            {"role": "user", "content": prompt}
        ],
    )

    return response.choices[0].message.content