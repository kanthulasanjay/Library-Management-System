import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

BOOKS_FILE = "data/books.csv"
USERS_FILE = "data/users.csv"
BORROW_FILE = "data/borrowed_books.csv"


# ------------------------
# Load Files
# ------------------------
def load_books():
    return pd.read_csv(BOOKS_FILE)


def load_users():
    return pd.read_csv(USERS_FILE)


def load_borrow():
    return pd.read_csv(BORROW_FILE)


def save_books(df):
    df.to_csv(BOOKS_FILE, index=False)


def save_borrow(df):
    df.to_csv(BORROW_FILE, index=False)


# ------------------------
# Borrow Menu
# ------------------------
def borrow_menu():

    st.title("📚 Borrow Management")

    tabs = st.tabs([
        "📖 Borrow Book",
        "🔄 Return Book",
        "📋 Borrow History"
    ])

    # ===================================================
    # Borrow Book
    # ===================================================
    with tabs[0]:

        books = load_books()
        users = load_users()

        available = books[
            books["available_copies"] > 0
        ]

        if available.empty:
            st.warning("No books available.")
            return

        user = st.selectbox(
            "Select User",
            users["user_id"]
        )

        book = st.selectbox(
            "Select Book",
            available["book_id"]
        )

        if st.button("Borrow Book"):

            borrow = load_borrow()

            issue = datetime.today()

            due = issue + timedelta(days=14)

            new = {
                "borrow_id": f"BR{len(borrow)+1:03}",
                "user_id": user,
                "book_id": book,
                "borrow_date": issue.date(),
                "due_date": due.date(),
                "return_date": "",
                "status": "Borrowed",
                "fine": 0
            }

            borrow = pd.concat(
                [borrow, pd.DataFrame([new])],
                ignore_index=True
            )

            idx = books[
                books["book_id"] == book
            ].index[0]

            books.loc[idx, "available_copies"] -= 1

            save_books(books)
            save_borrow(borrow)

            st.success("Book Borrowed Successfully!")

            st.rerun()

    # ===================================================
    # Return Book
    # ===================================================
    with tabs[1]:

        borrow = load_borrow()

        active = borrow[
            borrow["status"] == "Borrowed"
        ]

        if active.empty:
            st.info("No borrowed books.")
            return

        borrow_id = st.selectbox(
            "Borrow ID",
            active["borrow_id"]
        )

        if st.button("Return Book"):

            books = load_books()

            idx = borrow[
                borrow["borrow_id"] == borrow_id
            ].index[0]

            today = datetime.today().date()

            due = pd.to_datetime(
                borrow.loc[idx, "due_date"]
            ).date()

            fine = 0

            if today > due:
                fine = (today - due).days * 10

            borrow.loc[idx, "return_date"] = today
            borrow.loc[idx, "status"] = "Returned"
            borrow.loc[idx, "fine"] = fine

            book = borrow.loc[idx, "book_id"]

            b = books[
                books["book_id"] == book
            ].index[0]

            books.loc[b, "available_copies"] += 1

            save_books(books)
            save_borrow(borrow)

            st.success(
                f"Book Returned!\nFine: ₹{fine}"
            )

            st.rerun()

    # ===================================================
    # History
    # ===================================================
    with tabs[2]:

        borrow = load_borrow()

        user = st.text_input(
            "Search User ID"
        )

        if user:

            borrow = borrow[
                borrow["user_id"].str.contains(
                    user,
                    case=False,
                    na=False
                )
            ]

        st.dataframe(
            borrow,
            use_container_width=True,
            height=500
        )

        st.download_button(
            "📥 Download Borrow History",
            borrow.to_csv(index=False),
            "borrow_history.csv",
            "text/csv"
        )