import streamlit as st

from password_checker import analyze_password
from password_generator import generate_password


st.set_page_config(
    page_title="Password Strength Analyzer",
    page_icon="🔐",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background-color: #f5f7fb;
}

.main-title {
    font-size: 36px;
    font-weight: 800;
    color: #172554;
}

.subtitle {
    color: #64748b;
    font-size: 16px;
}

.metric-card {
    background: white;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #e2e8f0;
    text-align: center;
}

.section-title {
    color: #172554;
    font-size: 22px;
    font-weight: 700;
}

</style>
""", unsafe_allow_html=True)


if "generated_password" not in st.session_state:
    st.session_state.generated_password = ""

if "show_password" not in st.session_state:
    st.session_state.show_password = False

with st.sidebar:
    st.title("🔐 SecureCheck")
    st.caption("Password Security Analyzer")

    page = st.radio(
        "Navigation",
        ["Dashboard", "Password Generator", "About Project"]
    )

    st.divider()

    st.info(
        "Your password is analyzed locally by this application. "
        "It is not intentionally stored or transmitted."
    )

if page == "Dashboard":

    st.markdown(
        '<div class="main-title">Password Strength Analyzer</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Analyze your password security and improve your protection.</div>',
        unsafe_allow_html=True
    )

    st.write("")

    st.subheader("🔑 Enter Your Password")

    password = st.text_input(
        "Password",
        type="default" if st.session_state.show_password else "password",
        placeholder="Enter your password here",
        key="password_input"
    )

    st.session_state.show_password = st.checkbox(
        "Show password",
        value=st.session_state.show_password
    )

    if password:

        result = analyze_password(password)

        st.write("")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Strength", result["strength"])

        with col2:
            st.metric("Password Length", result["length"])

        with col3:
            st.metric("Security Score", f'{result["score"]}/4')

        st.write("### Password Strength Meter")

        st.progress(result["score"] / 4)

        if result["score"] <= 1:
            st.error("Your password needs improvement.")

        elif result["score"] == 2:
            st.warning("Your password has moderate strength.")

        elif result["score"] == 3:
            st.success("Your password is strong.")

        else:
            st.success("Excellent! Your password has very strong estimated strength.")

        st.divider()

        st.markdown(
            '<div class="section-title">Security Analysis</div>',
            unsafe_allow_html=True
        )

        for check, passed in result["checks"].items():

            if passed:
                st.success(f"✓ {check}")

            else:
                st.error(f"✗ {check}")

        st.divider()

        st.markdown(
            '<div class="section-title">Improvement Suggestions</div>',
            unsafe_allow_html=True
        )

        for suggestion in result["suggestions"]:
            st.write(f"💡 {suggestion}")

        if result["score"] == 4:
            st.success("Your password passed the strongest score level.")
        else:
            st.info("Consider using a randomly generated password.")

    else:
        st.info("Enter a password to start the security analysis.")

elif page == "Password Generator":

    st.title("🔐 Password Generator")

    st.write(
        "Generate a random password using a cryptographically secure "
        "random number generator."
    )

    length = st.slider(
        "Select Password Length",
        min_value=12,
        max_value=64,
        value=16
    )

    if st.button("Generate Secure Password", type="primary"):

        st.session_state.generated_password = generate_password(length)

    if st.session_state.generated_password:

        st.success("Password generated successfully!")

        st.code(st.session_state.generated_password)

        st.button(
            "Copy Password",
            on_click=lambda: st.toast(
                "Select and copy the password from the box above."
            )
        )

        st.caption(
            "For security, copy the password directly and save it "
            "in a trusted password manager."
        )


elif page == "About Project":

    st.title("About Password Strength Analyzer")

    st.write("""
    1.Project Objective

    The Password Strength Analyzer is a cybersecurity application
    designed to evaluate password security and help users create
    stronger passwords.

    2.Main Features

    - Password length analysis
    - Character complexity checking
    - Common password detection
    - Strength estimation using zxcvbn
    - Password improvement suggestions
    - Secure random password generation

    3.Technologies Used

    - Python
    - Streamlit
    - Regular Expressions
    - zxcvbn
    - Secrets module

    4.Security Concepts

    - Password entropy
    - Brute-force resistance
    - Password complexity
    - Cryptographically secure randomness

    5.Expected Outcome

    Learn practical password security concepts and basic
    cryptography through a working application.
    """)
    st.success("Developed using Python and Streamlit.")
