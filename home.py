import streamlit as st
import pandas as pd
from utils.icons import (
    icon_heading, kpi_card,
    BOOK_ICON, USERS_ICON, OPEN_BOOK_ICON, CHECK_ICON
)


def home_dashboard():

    books = pd.read_csv("data/books.csv")
    users = pd.read_csv("data/users.csv")
    borrow = pd.read_csv("data/borrowed_books.csv")

    total_books = len(books)
    total_users = len(users)
    borrowed = len(borrow[borrow["status"] == "Borrowed"])
    available = books["available_copies"].sum()

    st.markdown(
        icon_heading("Library Management System", icon=BOOK_ICON, size=30, tag="h1"),
        unsafe_allow_html=True
    )
    st.caption("Welcome back — here's what's happening in your library today.")
    st.write("")

    c1, c2, c3, c4 = st.columns(4)
    kpi_card(c1, BOOK_ICON, "Books", total_books, accent="blue")
    kpi_card(c2, USERS_ICON, "Users", total_users, accent="purple", color="#7C3AED")
    kpi_card(c3, OPEN_BOOK_ICON, "Borrowed", borrowed, accent="amber", color="#F59E0B")
    kpi_card(c4, CHECK_ICON, "Available", available, accent="green", color="#10B981")

    st.write("")
    st.divider()

    st.markdown("#### ✨ What you can do here")

    f1, f2, f3 = st.columns(3)

    with f1:
        with st.container(border=True):
            st.markdown("**📚 Manage Books**")
            st.caption("Add, update, remove, and search the catalog.")
        with st.container(border=True):
            st.markdown("**🔄 Borrow & Return**")
            st.caption("Track who has what, and when it's due.")

    with f2:
        with st.container(border=True):
            st.markdown("**👥 Manage Users**")
            st.caption("Students, teachers, and admins in one place.")
        with st.container(border=True):
            st.markdown("**💰 Fine Management**")
            st.caption("See pending fines and mark payments.")

    with f3:
        with st.container(border=True):
            st.markdown("**📊 Analytics Dashboard**")
            st.caption("Trends across categories, roles, and activity.")
        with st.container(border=True):
            st.markdown("**📈 Reports**")
            st.caption("Download CSVs for books, users, and history.")

    st.write("")
    st.info("Use the sidebar to navigate through the application.")