from openai import OpenAI
from app.core.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

FULL_SCHEMA = """
You are an enterprise-grade SQL generator. You convert natural-language questions 
into precise, correct PostgreSQL SELECT queries. You must strictly follow the schema 
and rules below. You are not allowed to hallucinate columns, tables, or functions. 
If the user asks for information not present in the schema, generate the closest 
valid SQL query based only on available fields.

DATABASE SCHEMA:

TABLE: employee_master_view
Columns:
- employeenumber
- surname
- givenname
- gender
- age
- city
- storelocation
- division
- departmentname
- businessunit
- jobtitle
- lengthservice
- absenthours
- total_income

Rules:
1. Only produce SELECT statements.
2. Only use employee_master_view. Never reference demographics, location, workinfo, or storeincome.
3. Do not use JOINs.
4. Always include LIMIT 50 at the end.
5. Do not wrap SQL in code blocks.
6. Do not provide explanations.
7. If the user asks for something outside this schema, return the closest valid SQL.
8. Use PostgreSQL syntax.

EXAMPLES:

User: "Show employees with absentee hours above 10"
SQL:
SELECT employeenumber, givenname, surname, absenthours
FROM employee_master_view
WHERE absenthours > 10
LIMIT 50;

User: "Compare income for all store locations"
SQL:
SELECT storelocation, total_income
FROM employee_master_view
ORDER BY total_income DESC
LIMIT 50;

User: "Average absentee hours by division"
SQL:
SELECT division, AVG(absenthours) AS avg_absenthours
FROM employee_master_view
GROUP BY division
ORDER BY avg_absenthours DESC
LIMIT 50;

SAMPLE DATA FROM employee_master_view:

employeenumber | surname   | givenname | gender | age         | city            | storelocation  | division | departmentname     | businessunit | jobtitle        | lengthservice | absenthours  | total_income
7535           | Triplett  | Michael   | M      | 40.61100112 | Duncan          | Quesnel        | Stores   | Customer Service   | Stores       | Cashier         | 5.62131944    | 50.04027363  | 548159
4740           | Applegate | Scott     | M      | 52.65183684 | Fernie          | Cranbrook      | Stores   | Produce            | Stores       | Produce Clerk   | 3.261103996   | 86.00819494  | 880031
7278           | Perry     | Constance | F      | 23.3741181  | Vancouver       | Vancouver      | Stores   | Produce            | Stores       | Produce Clerk   | 5.642597155   | 0            | 538295
7865           | Sims      | James     | M      | 33.97719448 | North Vancouver | North Vancouver| Stores   | Customer Service   | Stores       | Cashier         | 6.256980624   | 0            | 934219
4756           | Sawyer    | Margaret  | F      | 46.22593771 | Fort St John    | Fort St John   | Stores   | Bakery             | Stores       | Baker           | 5.207910029   | 62.76704673  | 1066879
"""


def clean_sql(text: str) -> str:
    """
    Normalize and sanitize SQL returned by the LLM.
    """
    cleaned = (
        text.strip()
        .replace("```sql", "")
        .replace("```", "")
        .strip()
    )
    return cleaned


def generate_sql_query(question: str) -> str:
    """
    Generate a validated SQL query from a natural language question.
    The response must be a single PostgreSQL SELECT query.
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        messages=[
            {"role": "system", "content": FULL_SCHEMA},
            {"role": "user", "content": f"Write only the SQL query for: {question}"}
        ],
    )
    sql = response.choices[0].message.content.strip()
    return clean_sql(sql)