import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000/chat/"

DIVISION_USERS = {
    "Infotech": "manager_infotech",
    "Executive": "manager_executive",
    "Finance and Accounting": "manager_finance",
    "Stores": "manager_stores",
    "HR": "manager_hr",
    "Legal": "manager_legal",
}

st.set_page_config(
    page_title="HR Analyst Chatbot",
    layout="centered",
)

st.title("HR Analyst Chatbot")

selected_user = st.selectbox(
    "Select Manager User",
    options=list(DIVISION_USERS.values()),
)

query = st.text_area("Ask a question", height=120)

submit = st.button("Submit")

if submit:
    if not query.strip():
        st.info("Please enter a valid question.")
    else:
        with st.spinner("Processing your request..."):
            try:
                response = requests.post(
                    API_URL,
                    json={"user_id": selected_user, "query": query},
                    timeout=60,
                )
            except Exception:
                st.success(
                    "Not able to provide those details currently, please try again."
                )
                st.stop()

        if response.status_code != 200:
            st.success(
                "Not able to provide those details currently, please try again."
            )
        else:
            data = response.json()
            answer = data.get("answer", "")
            sql = data.get("sql_used", "")
            rows = data.get("data", [])

            st.subheader("Answer")
            st.success(answer)

            with st.expander("Show SQL Query"):
                st.code(sql, language="sql")

            if rows:
                df = pd.DataFrame(rows)
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No rows returned.")