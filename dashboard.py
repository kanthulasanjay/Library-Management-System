import streamlit as st
import pandas as pd
from utils.books import books_menu
from utils.users import users_menu
from utils.borrow import borrow_menu
from utils.dashboard_stats import dashboard_stats
from utils.fines import fines_menu
from utils.home import home_dashboard
from utils.icons import (
    icon_heading, kpi_card,
    BOOK_ICON, USERS_ICON, OPEN_BOOK_ICON, CHECK_ICON
)


BOOKS_FILE = "data/books.csv"
USERS_FILE = "data/users.csv"
BORROW_FILE = "data/borrowed_books.csv"


def admin_dashboard():

    books = pd.read_csv(BOOKS_FILE)
    users = pd.read_csv(USERS_FILE)
    borrow = pd.read_csv(BORROW_FILE)

    st.markdown(
        icon_heading("Admin Dashboard", icon=BOOK_ICON, size=32, tag="h1"),
        unsafe_allow_html=True
    )
    st.caption("A quick, at-a-glance view of your library.")
    st.write("")

    total_books = len(books)
    available_books = books["available_copies"].sum()
    total_users = len(users)
    borrowed_books = len(borrow[borrow["status"] == "Borrowed"])

    c1, c2, c3, c4 = st.columns(4)

    kpi_card(c1, BOOK_ICON, "Total Books", total_books, accent="blue")
    kpi_card(c2, CHECK_ICON, "Available Copies", available_books, accent="green", color="#10B981")
    kpi_card(c3, USERS_ICON, "Total Users", total_users, accent="purple", color="#7C3AED")
    kpi_card(c4, OPEN_BOOK_ICON, "Borrowed Books", borrowed_books, accent="amber", color="#F59E0B")

    st.write("")
    st.divider()

    menu = st.sidebar.radio(
        "Admin Menu",
        [
            "Home",
            "Dashboard",
            "Books",
            "Users",
            "Borrow",
            "Fines"
        ]
    )

    if menu == "Home":
        home_dashboard()

    elif menu == "Dashboard":
        dashboard_stats()

    elif menu == "Books":
        books_menu()

    elif menu == "Users":
        users_menu()

    elif menu == "Borrow":
        borrow_menu()

    elif menu == "Fines":
        fines_menu()