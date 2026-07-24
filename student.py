import streamlit as st
import pandas as pd

BOOKS_FILE = "data/books.csv"
BORROW_FILE = "data/borrowed_books.csv"


def find_column(df, candidates):
    """Case-insensitive match against a list of likely column names."""
    lower_map = {c.lower(): c for c in df.columns}
    for candidate in candidates:
        if candidate.lower() in lower_map:
            return lower_map[candidate.lower()]
    return None


def student_dashboard(user):

    books = pd.read_csv(BOOKS_FILE)
    borrow = pd.read_csv(BORROW_FILE)

    # Only this student's records
    my_books = borrow[borrow["user_id"] == user["user_id"]]

    fine_col = find_column(borrow, ["fine", "fine_amount", "amount", "penalty"])
    total_fine = my_books[fine_col].sum() if fine_col else 0

    st.title(f"🎓 Welcome, {user['name']}")

    st.write(f"### 👋 Hello {user['name']}")
    st.write(f"**Role:** {user['role']}")

    st.divider()

    # ===========================
    # Dashboard Cards
    # ===========================
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "📚 Books Borrowed",
            len(my_books[my_books["status"] == "Borrowed"])
        )

    with col2:
        st.metric(
            "📖 Available Books",
            books["available_copies"].sum()
        )

    with col3:
        st.metric(
            "💰 Total Fine",
            f"₹ {total_fine:,.0f}"
        )

    st.divider()

    # ===========================
    # Borrow History
    # ===========================
    st.subheader("📋 My Borrow History")

    if my_books.empty:
        st.info("You haven't borrowed any books yet.")
    else:
        st.dataframe(
            my_books,
            use_container_width=True
        )

    st.divider()

    # ===========================
    # Available Books
    # ===========================
    st.subheader("📚 Available Books")

    available = books[
        books["available_copies"] > 0
    ]

    search = st.text_input("🔍 Search Book")

    if search:

        available = available[
            available["title"].str.contains(
                search,
                case=False,
                na=False
            )
        ]

    st.dataframe(
        available,
        use_container_width=True,
        height=350
    )

    st.download_button(
        "📥 Download My Borrow History",
        my_books.to_csv(index=False),
        "my_history.csv",
        "text/csv"
    )
     # ===========================
    # Borrow Book
    # ===========================
    st.subheader("📥 Borrow Book")

    if not available.empty:

        book_titles = available["title"].tolist()

        selected_book = st.selectbox(
            "Select Book",
            book_titles,
            key="borrow_book"
        )

        if st.button("Borrow Book"):

            row = books[books["title"] == selected_book].index[0]

            if books.loc[row, "available_copies"] > 0:

                books.loc[row, "available_copies"] -= 1

                borrow.loc[len(borrow)] = {
                    "user_id": user["user_id"],
                    "name": user["name"],
                    "book_id": books.loc[row, "book_id"],
                    "title": selected_book,
                    "borrow_date": pd.Timestamp.today().strftime("%Y-%m-%d"),
                    "return_date": "",
                    "status": "Borrowed",
                    "fine": 0
                }

                books.to_csv(BOOKS_FILE, index=False)
                borrow.to_csv(BORROW_FILE, index=False)

                st.success("Book borrowed successfully!")
                st.rerun()

            else:
                st.error("Book not available.")

    # ===========================
    # Return Book
    # ===========================
    st.subheader("📤 Return Book")

    borrowed = my_books[my_books["status"] == "Borrowed"]

    if borrowed.empty:

        st.info("No books to return.")

    else:

        # Merge borrowed books with books.csv to get book titles
        borrowed_books = borrowed.merge(
            books[["book_id", "title"]],
            on="book_id",
            how="left"
        )

        selected = st.selectbox(
            "Select Book",
            borrowed_books["title"].tolist(),
            key="return_book"
        )

        if st.button("Return Book"):

            # Get selected book_id
            selected_book_id = borrowed_books.loc[
                borrowed_books["title"] == selected,
                "book_id"
            ].iloc[0]

            # Update borrowed_books.csv
            idx = borrow[
                (borrow["user_id"] == user["user_id"]) &
                (borrow["book_id"] == selected_book_id) &
                (borrow["status"] == "Borrowed")
            ].index[0]

            borrow.loc[idx, "status"] = "Returned"
            borrow.loc[idx, "return_date"] = pd.Timestamp.today().strftime("%Y-%m-%d")

            # Increase available copies in books.csv
            book_idx = books[
                books["book_id"] == selected_book_id
            ].index[0]

            books.loc[book_idx, "available_copies"] += 1

            # Save changes
            books.to_csv(BOOKS_FILE, index=False)
            borrow.to_csv(BORROW_FILE, index=False)

            st.success("✅ Book returned successfully!")
            st.rerun()