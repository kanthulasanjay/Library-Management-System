import streamlit as st
import pandas as pd

USERS_FILE = "data/users.csv"


# ------------------------
# Load Users
# ------------------------
def load_users():
    return pd.read_csv(USERS_FILE)


# ------------------------
# Save Users
# ------------------------
def save_users(df):
    df.to_csv(USERS_FILE, index=False)


# ------------------------
# Users Menu
# ------------------------
def users_menu():

    users = load_users()

    st.title("👥 User Management")

    tabs = st.tabs([
        "👀 View Users",
        "➕ Add User",
        "✏️ Update User",
        "🗑 Delete User"
    ])

    # ==========================
    # VIEW USERS
    # ==========================
    with tabs[0]:

        c1, c2 = st.columns(2)

        name = c1.text_input("🔍 Search Name")

        username = c2.text_input("👤 Search Username")

        if name:
            users = users[
                users["name"].str.contains(
                    name,
                    case=False,
                    na=False
                )
            ]

        if username:
            users = users[
                users["username"].str.contains(
                    username,
                    case=False,
                    na=False
                )
            ]

        role = st.selectbox(
            "Filter Role",
            ["All"] + sorted(users["role"].unique()),
            key="users_filter_role"
        )

        if role != "All":
            users = users[
                users["role"] == role
            ]

        st.dataframe(
            users,
            use_container_width=True,
            height=500
        )

        st.download_button(
            "📥 Download Users",
            users.to_csv(index=False),
            "users.csv",
            "text/csv"
        )

    # ==========================
    # ADD USER
    # ==========================
    with tabs[1]:

        st.subheader("➕ Add User")

        name = st.text_input("Name")
        username = st.text_input("Username")
        password = st.text_input(
            "Password",
            type="password"
        )

        role = st.selectbox(
            "Role",
            ["Student", "Teacher", "Admin"],
            key="users_add_role"
        )

        email = st.text_input("Email")
        phone = st.text_input("Phone")

        if st.button("Add User"):

            new = {
                "user_id": f"U{len(load_users())+1:03}",
                "name": name,
                "username": username,
                "password": password,
                "role": role,
                "email": email,
                "phone": phone
            }

            df = pd.concat(
                [load_users(), pd.DataFrame([new])],
                ignore_index=True
            )

            save_users(df)

            st.success("User Added Successfully!")

            st.rerun()

    # ==========================
    # UPDATE USER
    # ==========================
    with tabs[2]:

        df = load_users()

        selected = st.selectbox(
            "Choose User",
            df["user_id"],
            key="users_update_choose"
        )

        row = df[
            df["user_id"] == selected
        ].iloc[0]

        name = st.text_input(
            "Name",
            row["name"]
        )

        username = st.text_input(
            "Username",
            row["username"]
        )

        password = st.text_input(
            "Password",
            row["password"]
        )

        role = st.selectbox(
            "Role",
            ["Student", "Teacher", "Admin"],
            index=["Student", "Teacher", "Admin"].index(row["role"]),
            key="users_update_role"
        )

        email = st.text_input(
            "Email",
            row["email"]
        )

        phone = st.text_input(
            "Phone",
            row["phone"]
        )

        if st.button("Update User"):

            idx = df[
                df["user_id"] == selected
            ].index[0]

            df.loc[idx] = [
                selected,
                name,
                username,
                password,
                role,
                email,
                phone
            ]

            save_users(df)

            st.success("User Updated!")

            st.rerun()

    # ==========================
    # DELETE USER
    # ==========================
    with tabs[3]:

        df = load_users()

        selected = st.selectbox(
            "Choose User",
            df["user_id"],
            key="users_delete_choose"
        )

        confirm = st.checkbox(
            "I understand this action."
        )

        if st.button("Delete User"):

            if confirm:

                df = df[
                    df["user_id"] != selected
                ]

                save_users(df)

                st.success("User Deleted Successfully!")

                st.rerun()

            else:

                st.warning(
                    "Please confirm deletion."
                )