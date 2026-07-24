import streamlit as st
import pandas as pd

BOOKS_FILE = "data/books.csv"


# -----------------------
# Load Books
# -----------------------
def load_books():
    return pd.read_csv(BOOKS_FILE)


# -----------------------
# Save Books
# -----------------------
def save_books(df):
    df.to_csv(BOOKS_FILE, index=False)


# -----------------------
# Resolve real column names
# -----------------------
def find_column(df, candidates):
    """Case-insensitive match against a list of likely column names."""
    lower_map = {c.lower(): c for c in df.columns}
    for candidate in candidates:
        if candidate.lower() in lower_map:
            return lower_map[candidate.lower()]
    return None


# -----------------------
# Books Menu
# -----------------------
def books_menu():

    books = load_books()

    qty_col = find_column(books, ["quantity", "total_copies", "total_quantity", "copies", "stock"])
    avail_col = find_column(books, ["available_copies", "available", "copies_available", "available_qty"])

    st.title("📚 Book Management")

    if not qty_col:
        st.warning(
            "Couldn't find a quantity column in books.csv. "
            f"Columns found: {', '.join(books.columns)}. "
            "Quantity fields below will be disabled until this is resolved."
        )

    menu = st.tabs([
        "📖 View",
        "➕ Add",
        "✏️ Update",
        "🗑 Delete"
    ])

    # ===================================
    # VIEW
    # ===================================
    with menu[0]:

        c1, c2 = st.columns(2)

        title = c1.text_input("🔍 Search Title")

        author = c2.text_input("✍ Search Author")

        if title:
            books = books[
                books["title"].str.contains(
                    title,
                    case=False,
                    na=False
                )
            ]

        if author:
            books = books[
                books["author"].str.contains(
                    author,
                    case=False,
                    na=False
                )
            ]

        if "category" in books.columns:

            category = st.selectbox(
                "Category",
                ["All"] + sorted(
                    books["category"].unique().tolist()
                ),
                key="books_view_category"
            )

            if category != "All":
                books = books[
                    books["category"] == category
                ]

        st.dataframe(
            books,
            use_container_width=True,
            height=500
        )

        st.download_button(
            "📥 Download CSV",
            books.to_csv(index=False),
            "books.csv",
            "text/csv"
        )

    # ===================================
    # ADD
    # ===================================
    with menu[1]:

        st.subheader("➕ Add Book")

        title = st.text_input("Book Title", key="books_add_title")

        author = st.text_input("Author", key="books_add_author")

        category = st.text_input("Category", key="books_add_category")

        quantity = st.number_input(
            "Quantity",
            min_value=1,
            value=1,
            key="books_add_quantity"
        )

        if st.button("Add Book", key="books_add_submit"):

            new = {
                "book_id": f"B{len(load_books())+1:03}",
                "title": title,
                "author": author,
                "category": category,
            }

            new[qty_col or "quantity"] = quantity
            new[avail_col or "available_copies"] = quantity

            df = pd.concat(
                [load_books(), pd.DataFrame([new])],
                ignore_index=True
            )

            save_books(df)

            st.success("Book Added Successfully!")

            st.rerun()

    # ===================================
    # UPDATE
    # ===================================
    with menu[2]:

        df = load_books()

        selected = st.selectbox(
            "Choose Book",
            df["book_id"],
            key="books_update_choose"
        )

        row = df[df["book_id"] == selected].iloc[0]

        title = st.text_input(
            "Title",
            row["title"],
            key="books_update_title"
        )

        author = st.text_input(
            "Author",
            row["author"],
            key="books_update_author"
        )

        category = st.text_input(
            "Category",
            row["category"],
            key="books_update_category"
        )

        if qty_col:
            quantity = st.number_input(
                "Quantity",
                value=int(row[qty_col]),
                key="books_update_quantity"
            )
        else:
            quantity = None

        if st.button("Update Book", key="books_update_submit"):

            idx = df[df["book_id"] == selected].index[0]

            df.loc[idx, "title"] = title
            df.loc[idx, "author"] = author
            df.loc[idx, "category"] = category

            if qty_col and quantity is not None:
                df.loc[idx, qty_col] = quantity

            save_books(df)

            st.success("Book Updated!")

            st.rerun()

    # ===================================
    # DELETE
    # ===================================
    with menu[3]:

        df = load_books()

        selected = st.selectbox(
            "Choose Book",
            df["book_id"],
            key="books_delete_choose"
        )

        confirm = st.checkbox(
            "I understand this action.",
            key="books_delete_confirm"
        )

        if st.button("Delete Book", key="books_delete_submit"):

            if confirm:

                df = df[
                    df["book_id"] != selected
                ]

                save_books(df)

                st.success("Book Deleted")

                st.rerun()

            else:
                st.warning(
                    "Please confirm deletion."
                )