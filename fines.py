import streamlit as st
import pandas as pd

FINES_FILE = "data/fines.csv"


# --------------------------
# Load Fines
# --------------------------
def load_fines():
    return pd.read_csv(FINES_FILE)


# --------------------------
# Save Fines
# --------------------------
def save_fines(df):
    df.to_csv(FINES_FILE, index=False)


# --------------------------
# Resolve real column names
# --------------------------
def find_column(df, candidates):
    """Case-insensitive match against a list of likely column names."""
    lower_map = {c.lower(): c for c in df.columns}
    for candidate in candidates:
        if candidate.lower() in lower_map:
            return lower_map[candidate.lower()]
    return None


# --------------------------
# Fine Menu
# --------------------------
def fines_menu():

    fines = load_fines()

    status_col = find_column(fines, ["status", "fine_status", "payment_status"])
    amount_col = find_column(fines, ["amount", "fine_amount", "amount_due", "fine"])

    st.title("💰 Fine Management")

    if not status_col or not amount_col:
        st.error(
            "fines.csv is missing a recognizable status/amount column. "
            f"Columns found: {', '.join(fines.columns)}. "
            "Expected something like 'status' and 'amount'."
        )
        return

    tab1, tab2 = st.tabs([
        "📋 View Fines",
        "💳 Update Payment"
    ])

    # ==========================
    # VIEW FINES
    # ==========================
    with tab1:

        col1, col2 = st.columns(2)

        user = col1.text_input("Search User ID")

        status = col2.selectbox(
            "Status",
            ["All", "Pending", "Paid"]
        )

        data = fines.copy()

        if user:
            data = data[
                data["user_id"].astype(str).str.contains(
                    user,
                    case=False,
                    na=False
                )
            ]

        if status != "All":
            data = data[
                data[status_col] == status
            ]

        st.dataframe(
            data,
            use_container_width=True,
            height=450
        )

        st.download_button(
            "📥 Download Fines",
            data.to_csv(index=False),
            "fines.csv",
            "text/csv"
        )

        st.divider()

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Total Records",
            len(fines)
        )

        c2.metric(
            "Pending",
            len(fines[fines[status_col] == "Pending"])
        )

        c3.metric(
            "Collected Amount",
            f"₹ {fines[fines[status_col]=='Paid'][amount_col].sum():,.0f}"
        )

    # ==========================
    # UPDATE PAYMENT
    # ==========================
    with tab2:

        pending = fines[
            fines[status_col] == "Pending"
        ]

        if pending.empty:
            st.success("No Pending Fines 🎉")
            return

        fine = st.selectbox(
            "Fine ID",
            pending["fine_id"]
        )

        if st.button(
            "Mark as Paid",
            use_container_width=True
        ):

            idx = fines[
                fines["fine_id"] == fine
            ].index[0]

            fines.loc[idx, status_col] = "Paid"

            save_fines(fines)

            st.success("Payment Updated Successfully!")

            st.rerun()