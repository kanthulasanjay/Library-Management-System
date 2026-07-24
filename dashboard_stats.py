import streamlit as st
import pandas as pd
import plotly.express as px
from utils.icons import icon_heading, CHART_ICON

BOOKS_FILE = "data/books.csv"
USERS_FILE = "data/users.csv"
BORROW_FILE = "data/borrowed_books.csv"
FINES_FILE = "data/fines.csv"

# Soft, light-friendly palette shared across all charts
PALETTE = ["#2563EB", "#7C3AED", "#0EA5E9", "#F59E0B", "#10B981", "#EC4899"]


def find_column(df, candidates):
    """Case-insensitive match against a list of likely column names."""
    lower_map = {c.lower(): c for c in df.columns}
    for candidate in candidates:
        if candidate.lower() in lower_map:
            return lower_map[candidate.lower()]
    return None


def styled_chart(fig, height=360):
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#1E293B", size=13),
        title_font=dict(color="#0F172A", size=15),
        margin=dict(l=10, r=10, t=45, b=10),
        height=height,
        legend=dict(orientation="h", yanchor="bottom", y=-0.25),
        colorway=PALETTE,
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=True, gridcolor="#E2E8F0")
    st.plotly_chart(fig, use_container_width=True)


def dashboard_stats():

    books = pd.read_csv(BOOKS_FILE)
    users = pd.read_csv(USERS_FILE)
    borrow = pd.read_csv(BORROW_FILE)
    fines = pd.read_csv(FINES_FILE)

    st.markdown(
        icon_heading("Library Statistics", icon=CHART_ICON, size=30, tag="h2"),
        unsafe_allow_html=True
    )
    st.caption("Trends and breakdowns across books, users, and activity.")
    st.write("")

    # ===============================
    # Row 1
    # ===============================
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 📚 Books by Category")

        category = (
            books.groupby("category")
            .size()
            .reset_index(name="Count")
        )

        fig = px.pie(
            category,
            names="category",
            values="Count",
            hole=0.55,
            color_discrete_sequence=PALETTE,
        )
        fig.update_traces(textinfo="percent+label")
        styled_chart(fig)

    with col2:
        st.markdown("#### 👥 Users by Role")

        role = (
            users.groupby("role")
            .size()
            .reset_index(name="Count")
        )

        fig = px.bar(
            role,
            x="role",
            y="Count",
            text="Count",
            color="role",
            color_discrete_sequence=PALETTE,
        )
        fig.update_traces(textposition="outside", showlegend=False)
        styled_chart(fig)

    st.divider()

    # ===============================
    # Row 2
    # ===============================
    col3, col4 = st.columns(2)

    with col3:
        st.markdown("#### 📖 Borrow Status")

        status = (
            borrow.groupby("status")
            .size()
            .reset_index(name="Count")
        )

        fig = px.pie(
            status,
            names="status",
            values="Count",
            hole=0.55,
            color_discrete_sequence=PALETTE,
        )
        fig.update_traces(textinfo="percent+label")
        styled_chart(fig)

    with col4:
        st.markdown("#### 💰 Fine Collection")

        status_col = find_column(fines, ["status", "fine_status", "payment_status"])
        amount_col = find_column(fines, ["amount", "fine_amount", "amount_due", "fine"])

        if status_col and amount_col:

            fine = (
                fines.groupby(status_col)[amount_col]
                .sum()
                .reset_index()
            )

            fig = px.bar(
                fine,
                x=status_col,
                y=amount_col,
                text=amount_col,
                color=status_col,
                color_discrete_sequence=[PALETTE[3], PALETTE[4]],
            )
            fig.update_traces(textposition="outside", showlegend=False)
            styled_chart(fig)

        else:
            st.warning(
                f"Couldn't find a status/amount column in fines.csv. "
                f"Columns found: {', '.join(fines.columns)}"
            )

    st.divider()

    # ===============================
    # Monthly Borrow Trend
    # ===============================
    st.markdown("#### 📈 Monthly Borrow Trend")

    borrow["borrow_date"] = pd.to_datetime(
        borrow["borrow_date"],
        errors="coerce"
    )

    monthly = (
        borrow.groupby(
            borrow["borrow_date"].dt.to_period("M")
        )
        .size()
        .reset_index(name="Borrow Count")
    )

    monthly["borrow_date"] = monthly["borrow_date"].astype(str)

    fig = px.line(
        monthly,
        x="borrow_date",
        y="Borrow Count",
        markers=True,
        color_discrete_sequence=[PALETTE[0]],
    )
    fig.update_traces(line=dict(width=3), marker=dict(size=8))
    styled_chart(fig, height=380)