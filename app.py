import streamlit as st
import duckdb
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# --------------------------------------------------
# Page config
# --------------------------------------------------
st.set_page_config(
    page_title="SaaS Funnel Analytics",
    layout="wide"
)

st.title("📊 SaaS Funnel Analytics Dashboard")

# --------------------------------------------------
# Database connection (READ ONLY, cached)
# --------------------------------------------------
BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "sql" / "saas.db"

@st.cache_resource
def get_connection():
    return duckdb.connect(str(DB_PATH), read_only=True)

con = get_connection()

st.caption(f"Using DB at: `{DB_PATH}`")
st.success("Connected to database")

# --------------------------------------------------
# Optional: view tables
# --------------------------------------------------
with st.expander("📂 View tables"):
    st.write(con.execute("SHOW TABLES").fetchall())

# --------------------------------------------------
# Tabs
# --------------------------------------------------
tab_funnel, tab_retention, tab_churn = st.tabs(
    ["🔻 Funnel", "📈 Retention", "📉 Churn"]
)

# ==================================================
# FUNNEL TAB
# ==================================================
with tab_funnel:
    st.header("🔻 Funnel Overview")

    df_funnel = con.execute(
        open("sql/funnel.sql").read()
    ).fetchdf()

    total_users = int(df_funnel["total_users"][0])
    activated_users = int(df_funnel["activated_users"][0])
    paid_users = int(df_funnel["paid_users"][0])

    activation_rate = round((activated_users / total_users) * 100, 1)
    paid_rate = round((paid_users / activated_users) * 100, 1)
    drop_off = round(100 - paid_rate, 1)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Signups", f"{total_users:,}")
    col2.metric("Activated", f"{activated_users:,}", f"{activation_rate}%")
    col3.metric("Paid", f"{paid_users:,}", f"{paid_rate}%")
    col4.metric("Drop-off", f"{drop_off}%")

    st.subheader("Signup → Activation → Paid")

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar(
        ["Signup", "Activated", "Paid"],
        [total_users, activated_users, paid_users]
    )
    ax.set_ylabel("Users")
    ax.set_title("SaaS Funnel")
    st.pyplot(fig, use_container_width=True)

# ==================================================
# RETENTION TAB
# ==================================================
with tab_retention:
    st.header("📈 Retention (Weekly Cohorts)")
    st.caption("Percentage of users retained across weeks per signup cohort")

    df_ret = con.execute(
        open("sql/retention.sql").read()
    ).fetchdf()

    # ---- FIX cohort date + formatting ----
    df_ret["cohort_date"] = pd.to_datetime(
        df_ret["cohort_date"]
    ).dt.strftime("%Y-%m-%d")

    df_ret["week_number"] = df_ret["week_number"].astype(int)
    df_ret["retention_percentage"] = df_ret["retention_percentage"].round(1)

    retention_matrix = df_ret.pivot(
        index="cohort_date",
        columns="week_number",
        values="retention_percentage"
    ).fillna(0)

    with st.expander("📊 View retention table"):
        st.dataframe(
            retention_matrix,
            use_container_width=True,
            height=420
        )

# ==================================================
# CHURN TAB
# ==================================================
with tab_churn:
    st.header("📉 Churn Analysis")

    df_churn = con.execute(
        open("sql/churn.sql").read()
    ).fetchdf()

    total_users = int(df_churn["total_users"][0])
    churned_users = int(df_churn["churned_users"][0])
    churn_rate = float(df_churn["churn_rate"][0])

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Activated Users", f"{total_users:,}")
    col2.metric("Churned Users", f"{churned_users:,}")
    col3.metric("Churn Rate", f"{churn_rate:.1f}%")

    if churn_rate > 50:
        st.warning("⚠️ High churn detected. Retention strategy needs improvement.")
    elif churn_rate > 25:
        st.info("📉 Moderate churn. Optimization opportunity.")
    else:
        st.success("✅ Healthy churn rate.")

    with st.expander("📄 Raw churn data"):
        st.dataframe(df_churn, use_container_width=True)

# --------------------------------------------------
# Footer
# --------------------------------------------------
st.caption(
    "Data is simulated for analytics & portfolio demonstration purposes."
)
