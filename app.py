import streamlit as st
from utils.auth import authenticate
from utils.dashboard import admin_dashboard
from utils.student import student_dashboard
from utils.teacher import teacher_dashboard
from utils.icons import icon_heading, BOOK_ICON, LOCK_ICON

# -------------------------------------------------
# Page Configuration
# -------------------------------------------------
st.set_page_config(
    page_title="Library Management System",
    page_icon="📚",
    layout="wide"
)

# -------------------------------------------------
# Load Custom CSS
# -------------------------------------------------
with open("assets/style.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

# -------------------------------------------------
# Session State
# -------------------------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None

# =================================================
# LOGIN PAGE
# =================================================
if not st.session_state.logged_in:

    # Logo + Title (side by side)
    import base64

    with open("assets/library.png", "rb") as f:
        logo_base64 = base64.b64encode(f.read()).decode()

    st.markdown(
        f"""
        <div style="display:flex; align-items:center; justify-content:center; gap:18px; margin-top:10px;">
            <img src="data:image/png;base64,{logo_base64}" width="90" />
            <h1 style="margin:0;">Library Management System</h1>
        </div>
        <p style="text-align:center; font-size:22px; color:gray; margin-top:12px;">
            Manage books, users, and borrowing records efficiently.
        </p>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    # Login Card
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        with st.container(border=True):

            st.markdown(
                icon_heading("Login", icon=LOCK_ICON, size=22, color="#0F172A", tag="h3", gradient=False),
                unsafe_allow_html=True
            )

            username = st.text_input("Username")

            password = st.text_input(
                "Password",
                type="password"
            )

            if st.button(
                "Login",
                use_container_width=True
            ):

                user = authenticate(
                    username,
                    password
                )

                if user:

                    st.session_state.logged_in = True
                    st.session_state.user = user

                    st.success(
                        f"Welcome {user['name']}!"
                    )

                    st.rerun()

                else:

                    st.error(
                        "❌ Invalid Username or Password"
                    )

    st.divider()

    st.caption(
        "© 2026 Library Management System | Python • Streamlit • Pandas"
    )

# =================================================
# DASHBOARD
# =================================================
else:

    user = st.session_state.user

    # Sidebar
    st.sidebar.image(
        "assets/library.png",
        width=120
    )

    st.sidebar.markdown(
        icon_heading("Library Management", icon=BOOK_ICON, size=24, tag="h2"),
        unsafe_allow_html=True
    )
    st.sidebar.success("Logged In")

    st.sidebar.write(f"👤 **Name:** {user['name']}")
    st.sidebar.write(f"🎓 **Role:** {user['role']}")

    st.sidebar.divider()

    if st.sidebar.button("Logout"):

        st.session_state.logged_in = False
        st.session_state.user = None

        st.rerun()

    # Dashboard by Role
    if user["role"] == "Admin":
        admin_dashboard()

    elif user["role"] == "Student":
        student_dashboard(user)

    elif user["role"] == "Teacher":
        teacher_dashboard(user)

    else:
        st.error("Invalid User Role")