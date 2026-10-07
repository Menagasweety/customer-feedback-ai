import html

import streamlit as st
import streamlit.components.v1 as components

from src.data_processing import load_data, get_dashboard_metrics
from src.complaint_analysis import (
    get_critical_reviews,
    analyze_complaints,
    find_complaint_categories,
)
from src.gemini_response import generate_email, MODEL_NAME


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Customer Feedback AI",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# SESSION STATE
# ============================================================

if "gemini_api_key" not in st.session_state:
    st.session_state.gemini_api_key = ""

if "generated_email" not in st.session_state:
    st.session_state.generated_email = ""

if "my_review_email" not in st.session_state:
    st.session_state.my_review_email = ""


# ============================================================
# GLOBAL CSS
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background:
            radial-gradient(
                circle at 10% 0%,
                rgba(99, 102, 241, 0.10),
                transparent 30%
            ),
            radial-gradient(
                circle at 90% 10%,
                rgba(79, 70, 229, 0.07),
                transparent 25%
            ),
            #080c14;
    }

    .block-container {
        max-width: 1450px;
        padding-top: 2rem;
        padding-bottom: 4rem;
        padding-left: 3rem;
        padding-right: 3rem;
    }

    section[data-testid="stSidebar"] {
        background: #0b111d;
        border-right: 1px solid #1e293b;
    }

    div[data-baseweb="input"] > div,
    div[data-baseweb="textarea"] > div,
    div[data-baseweb="select"] > div {
        background-color: #111827 !important;
        border-color: #293548 !important;
        border-radius: 10px !important;
    }

    input,
    textarea {
        color: #f8fafc !important;
    }

    input::placeholder,
    textarea::placeholder {
        color: #64748b !important;
    }

    div.stButton > button {
        min-height: 43px;
        border-radius: 10px;
        font-weight: 650;
        border: 1px solid #34415a;
    }

    div.stButton > button:hover {
        border-color: #818cf8;
    }

    div.stButton > button[kind="primary"] {
        background: linear-gradient(
            135deg,
            #4f46e5,
            #6366f1
        ) !important;

        color: white !important;
        border: none !important;
    }

    hr {
        border-color: #1e293b !important;
    }

    .sidebar-title {
        color: #f8fafc;
        font-size: 21px;
        font-weight: 800;
        margin-bottom: 5px;
    }

    .sidebar-description {
        color: #94a3b8;
        font-size: 12px;
        line-height: 1.55;
        margin-bottom: 25px;
    }

    .sidebar-note {
        color: #64748b;
        font-size: 11px;
        line-height: 1.6;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def find_column(row, possible_columns):
    for column in possible_columns:
        if column in row.index:
            return column

    return None


def get_product_name(row):
    column = find_column(
        row,
        [
            "product",
            "product_name",
            "Product",
        ],
    )

    if column is None:
        return "Unknown Product"

    value = row[column]

    if value is None:
        return "Unknown Product"

    return str(value)


def get_rating(row):
    column = find_column(
        row,
        [
            "stars",
            "rating",
            "Rating",
        ],
    )

    if column is None:
        return 1

    try:
        return int(row[column])
    except (ValueError, TypeError):
        return 1


def get_review_text(row):
    column = find_column(
        row,
        [
            "comments",
            "review_text",
            "review",
            "comment",
            "text",
        ],
    )

    if column is None:
        return ""

    value = row[column]

    if value is None:
        return ""

    return str(value)


def get_review_title(row):
    column = find_column(
        row,
        [
            "title",
            "Title",
        ],
    )

    if column is None:
        return ""

    value = row[column]

    if value is None:
        return ""

    return str(value)


def render_metric(label, value, note):

    st.html(
        f"""
        <div style="
            background:#111827;
            border:1px solid #253147;
            border-radius:15px;
            padding:20px 21px;
            min-height:105px;
            box-sizing:border-box;
        ">

            <div style="
                color:#94a3b8;
                font-size:13px;
                margin-bottom:8px;
            ">
                {html.escape(str(label))}
            </div>

            <div style="
                color:#f8fafc;
                font-size:28px;
                font-weight:800;
                line-height:1.1;
            ">
                {html.escape(str(value))}
            </div>

            <div style="
                color:#64748b;
                font-size:11px;
                margin-top:7px;
            ">
                {html.escape(str(note))}
            </div>

        </div>
        """
    )


def render_review_card(
    product,
    rating,
    title,
    review_text,
):

    safe_product = html.escape(str(product))
    safe_title = html.escape(str(title))
    safe_review = html.escape(str(review_text))

    stars = "★" * max(1, min(5, int(rating)))

    title_html = ""

    if str(title).strip():

        title_html = f"""
        <div style="
            color:#94a3b8;
            font-size:13px;
            margin-bottom:13px;
        ">
            {safe_title}
        </div>
        """

    st.html(
        f"""
        <div style="
            background:#111827;
            border:1px solid #253147;
            border-radius:15px;
            padding:23px;
            margin-top:8px;
            box-sizing:border-box;
        ">

            <div style="
                color:#fb7185;
                font-size:14px;
                font-weight:700;
                margin-bottom:6px;
            ">
                {stars}
                &nbsp;&nbsp;
                {int(rating)}/5
            </div>

            <div style="
                color:#f8fafc;
                font-size:19px;
                font-weight:750;
                margin-bottom:5px;
            ">
                {safe_product}
            </div>

            {title_html}

            <div style="
                color:#cbd5e1;
                font-size:14px;
                line-height:1.7;
            ">
                {safe_review}
            </div>

        </div>
        """
    )


def render_email_editor(email_text, height=450):

    safe_email = html.escape(str(email_text))

    editor_html = f"""
    <!DOCTYPE html>

    <html>

    <head>

        <style>

            html,
            body {{
                margin:0;
                padding:0;
                background:transparent;
                font-family:Arial,sans-serif;
            }}

            .email-wrapper {{
                width:100%;
                box-sizing:border-box;

                background:#111827;

                border:1px solid #293548;
                border-radius:14px;

                overflow:hidden;
            }}

            .email-editor {{
                display:block;

                width:100%;
                min-height:345px;

                box-sizing:border-box;

                resize:vertical;

                border:none;
                outline:none;

                padding:22px;

                background:#111827;
                color:#f8fafc;

                font-family:Arial,sans-serif;
                font-size:15px;
                line-height:1.7;
            }}

            .email-toolbar {{
                display:flex;
                justify-content:flex-end;
                align-items:center;

                gap:12px;

                padding:11px 14px;

                background:#0d1422;

                border-top:1px solid #293548;
            }}

            .copy-status {{
                color:#94a3b8;
                font-size:13px;
            }}

            .copy-button {{
                background:#4f46e5;
                color:white;

                border:none;
                border-radius:8px;

                padding:9px 16px;

                font-size:14px;
                font-weight:650;

                cursor:pointer;
            }}

            .copy-button:hover {{
                background:#6366f1;
            }}

        </style>

    </head>

    <body>

        <div class="email-wrapper">

            <textarea
                id="emailEditor"
                class="email-editor"
            >{safe_email}</textarea>

            <div class="email-toolbar">

                <span
                    id="copyStatus"
                    class="copy-status"
                ></span>

                <button
                    class="copy-button"
                    onclick="copyEmail()"
                >
                    📋 Copy Email
                </button>

            </div>

        </div>


        <script>

            async function copyEmail() {{

                const editor =
                    document.getElementById("emailEditor");

                const status =
                    document.getElementById("copyStatus");

                const text = editor.value;

                try {{

                    await navigator.clipboard.writeText(text);

                    status.textContent = "Copied!";

                    setTimeout(function() {{
                        status.textContent = "";
                    }}, 1800);

                }} catch (error) {{

                    editor.focus();
                    editor.select();

                    try {{

                        document.execCommand("copy");

                        status.textContent = "Copied!";

                    }} catch (fallbackError) {{

                        status.textContent =
                            "Please copy manually";

                    }}

                    setTimeout(function() {{
                        status.textContent = "";
                    }}, 2200);
                }}
            }}

        </script>

    </body>

    </html>
    """

    components.html(
        editor_html,
        height=height,
        scrolling=False,
    )


# ============================================================
# LOAD DATA
# ============================================================

try:

    df = load_data()

except Exception as error:

    st.error(
        "The dataset could not be loaded."
    )

    st.exception(error)

    st.stop()


# ============================================================
# SIDEBAR — SECURITY / API KEY
# ============================================================

with st.sidebar:

    st.html(
        """
        <div class="sidebar-title">
            💬 Customer Feedback AI
        </div>

        <div class="sidebar-description">
            Rule-based customer feedback triage with
            Gemini-powered response drafting.
        </div>
        """
    )

    st.markdown("### Gemini API")

    st.caption(
        "Enter your API key only when you want to "
        "generate a response."
    )


    # --------------------------------------------------------
    # API KEY INPUT
    # --------------------------------------------------------

    api_key = st.text_input(
        "Gemini API Key",
        type="password",
        value=st.session_state.gemini_api_key,
        placeholder="Enter API key",
    )

    st.session_state.gemini_api_key = api_key


    # --------------------------------------------------------
    # ACTIVE KEY
    # --------------------------------------------------------

    if st.session_state.gemini_api_key:

        st.success("API key active")


        # ----------------------------------------------------
        # DELETE FROM CURRENT SESSION
        # ----------------------------------------------------

        if st.button(
            "🗑️ Delete API Key from Session",
            use_container_width=True,
        ):

            st.session_state.gemini_api_key = ""
            st.session_state.generated_email = ""
            st.session_state.my_review_email = ""

            st.rerun()


        # ----------------------------------------------------
        # GOOGLE-SIDE KEY MANAGEMENT
        # ----------------------------------------------------

        st.markdown("#### Permanent key management")

        st.caption(
            "Permanent deletion must be performed in "
            "Google's API-key manager. The Gemini API key "
            "itself does not have permission to delete itself."
        )

        st.link_button(
            "🔐 Manage / Delete Key in Google",
            "https://aistudio.google.com/app/apikey",
            use_container_width=True,
        )


        st.warning(
            "Deleting the key in Google makes it unusable. "
            "Google may retain a deleted key for up to "
            "30 days before permanent removal."
        )


    else:

        st.info(
            "No API key stored in this session."
        )


    # --------------------------------------------------------
    # SECURITY INFORMATION
    # --------------------------------------------------------

    st.divider()

    st.markdown("### Security")

    st.html(
        """
        <div class="sidebar-note">

            🔒 The API key is entered as a password field.

            <br><br>

            🔒 The key is kept only in the current
            Streamlit session.

            <br><br>

            🔒 It is not written into the application
            source code.

            <br><br>

            🔒 It is not automatically saved to
            browser storage.

            <br><br>

            🗑️ "Delete from Session" removes the key
            from this running application session.

            <br><br>

            🔐 Google-side deletion is handled through
            Google's official API-key management system.

        </div>
        """
    )


    st.divider()

    st.markdown("### Gemini Model")

    st.caption(
        str(MODEL_NAME)
    )


# ============================================================
# HERO
# ============================================================

st.html(
    f"""
    <div style="
        background:
            linear-gradient(
                135deg,
                rgba(79,70,229,0.20),
                rgba(17,24,39,0.96)
            );

        border:1px solid #293548;
        border-radius:20px;

        padding:34px 38px;

        margin-bottom:30px;

        box-shadow:
            0 15px 40px rgba(0,0,0,0.18);
    ">

        <div style="
            color:#f8fafc;
            font-size:34px;
            font-weight:800;
            letter-spacing:-0.8px;
            margin-bottom:8px;
        ">
            💬 Customer Feedback AI Assistant
        </div>

        <div style="
            color:#94a3b8;
            font-size:15px;
            line-height:1.65;
            max-width:850px;
        ">
            Analyze critical customer feedback using
            rule-based logic and use Gemini to draft
            concise, empathetic customer-support responses.
        </div>

        <div style="
            display:inline-block;
            margin-top:17px;

            padding:7px 13px;

            border-radius:999px;

            background:rgba(99,102,241,0.14);

            border:1px solid rgba(129,140,248,0.30);

            color:#a5b4fc;

            font-size:12px;
            font-weight:650;
        ">
            Gemini • {html.escape(str(MODEL_NAME))}
        </div>

    </div>
    """
)


# ============================================================
# DASHBOARD
# ============================================================

st.markdown("## Feedback Dashboard")

st.caption(
    "Overview of the customer review dataset and "
    "rule-based critical feedback."
)

try:
    get_dashboard_metrics(df)
except Exception:
    pass


critical_df = get_critical_reviews(df)

total_reviews = len(df)

critical_count = len(critical_df)

if total_reviews > 0:

    critical_percentage = (
        critical_count / total_reviews
    ) * 100

else:

    critical_percentage = 0


# ============================================================
# COMPLAINT CATEGORIES
# ============================================================

try:

    complaint_counts = analyze_complaints(
        critical_df
    )

    if hasattr(
        complaint_counts,
        "shape",
    ):

        complaint_category_count = (
            complaint_counts.shape[0]
        )

    elif isinstance(
        complaint_counts,
        dict,
    ):

        complaint_category_count = (
            len(complaint_counts)
        )

    else:

        complaint_category_count = (
            len(complaint_counts)
            if hasattr(
                complaint_counts,
                "__len__"
            )
            else 0
        )

except Exception:

    complaint_counts = {}

    complaint_category_count = 0


# ============================================================
# METRICS
# ============================================================

col1, col2, col3, col4 = st.columns(
    4,
    gap="medium",
)

with col1:

    render_metric(
        "Total Reviews",
        f"{total_reviews:,}",
        "Reviews in dataset",
    )

with col2:

    render_metric(
        "Critical Reviews",
        f"{critical_count:,}",
        "Ratings ≤ 2",
    )

with col3:

    render_metric(
        "Critical Rate",
        f"{critical_percentage:.2f}%",
        "Share of all reviews",
    )

with col4:

    render_metric(
        "Complaint Categories",
        complaint_category_count,
        "Rule-based categories",
    )


# ============================================================
# CRITICAL REVIEW EXPLORER
# ============================================================

st.markdown("---")

st.markdown("## Critical Review Explorer")

st.caption(
    "Select a critical review and generate an "
    "empathetic response using Gemini."
)


if len(critical_df) == 0:

    st.warning(
        "No critical reviews were found."
    )

else:

    review_options = []

    for index, row in critical_df.iterrows():

        product = get_product_name(row)

        rating = get_rating(row)

        title = get_review_title(row)

        if title.strip():

            label = (
                f"{product} • "
                f"{rating}★ • "
                f"{title}"
            )

        else:

            label = (
                f"{product} • "
                f"{rating}★ • "
                f"Review {index}"
            )

        review_options.append(
            (index, label)
        )


    selected_review = st.selectbox(
        "Select a critical review",
        review_options,
        format_func=lambda item: item[1],
    )


    selected_index = selected_review[0]

    selected_row = critical_df.loc[
        selected_index
    ]


    selected_product = get_product_name(
        selected_row
    )

    selected_rating = get_rating(
        selected_row
    )

    selected_title = get_review_title(
        selected_row
    )

    selected_text = get_review_text(
        selected_row
    )


    render_review_card(
        product=selected_product,
        rating=selected_rating,
        title=selected_title,
        review_text=selected_text,
    )


    st.write("")


    generate_existing = st.button(
        "✨ Generate Response for This Review",
        type="primary",
        use_container_width=True,
    )


    if generate_existing:

        if not st.session_state.gemini_api_key:

            st.warning(
                "Enter your Gemini API key in the sidebar first."
            )

        elif not selected_text.strip():

            st.warning(
                "This review does not contain usable review text."
            )

        else:

            with st.spinner(
                "Generating response with Gemini..."
            ):

                try:

                    response = generate_email(
                        api_key=(
                            st.session_state
                            .gemini_api_key
                        ),

                        product=(
                            selected_product
                        ),

                        rating=(
                            selected_rating
                        ),

                        review_text=(
                            selected_text
                        ),

                        categories=find_complaint_categories(
                            selected_text
                        ),
                    )

                    st.session_state.generated_email = (
                        response
                    )

                except Exception as error:

                    st.error(
                        "Gemini could not generate the response."
                    )

                    st.exception(error)


# ============================================================
# GENERATED EMAIL — EXISTING REVIEW
# ============================================================

if st.session_state.generated_email:

    st.markdown("---")

    st.markdown("## Generated Response")

    st.caption(
        "Edit the draft directly and copy the final "
        "version when you are satisfied with it."
    )

    render_email_editor(
        st.session_state.generated_email,
        height=450,
    )

    st.caption(
        "Human review required. This application "
        "does not send emails automatically."
    )


# ============================================================
# MY OWN REVIEW
# ============================================================

st.markdown("---")

st.markdown("## Test Gemini With Your Own Review")

st.caption(
    "Enter a product, rating, and customer comment "
    "to test Gemini with your own feedback."
)


product_name = st.text_input(
    "Product name",
    placeholder="Example: Wireless Headphones",
)


rating = st.slider(
    "Star rating",
    min_value=1,
    max_value=5,
    value=1,
    step=1,
)


customer_comment = st.text_area(
    "Customer comment",
    placeholder=(
        "Example: The headphones stopped working after "
        "a few days and the sound quality is poor."
    ),
    height=180,
)


generate_my_review = st.button(
    "✨ Generate Response",
    type="primary",
    use_container_width=True,
)


# ============================================================
# GENERATE OWN REVIEW
# ============================================================

if generate_my_review:

    if not st.session_state.gemini_api_key:

        st.warning(
            "Enter your Gemini API key in the sidebar first."
        )

    elif not product_name.strip():

        st.warning(
            "Please enter a product name."
        )

    elif not customer_comment.strip():

        st.warning(
            "Please enter the customer comment."
        )

    else:

        with st.spinner(
            "Generating your personalized response..."
        ):

            try:

                response = generate_email(
                    api_key=(
                        st.session_state
                        .gemini_api_key
                    ),

                    product=(
                        product_name.strip()
                    ),

                    rating=rating,

                    review_text=(
                        customer_comment.strip()
                    ),

                    categories=find_complaint_categories(
                        customer_comment.strip()
                    ),
                )

                st.session_state.my_review_email = (
                    response
                )

            except Exception as error:

                st.error(
                    "Gemini could not generate the response."
                )

                st.exception(error)


# ============================================================
# GENERATED EMAIL — OWN REVIEW
# ============================================================

if st.session_state.my_review_email:

    st.markdown("---")

    st.markdown("## Your Generated Email")

    st.caption(
        "Edit the email directly, then use Copy Email."
    )

    render_email_editor(
        st.session_state.my_review_email,
        height=450,
    )

    st.caption(
        "Human review required. No email is sent automatically."
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.html(
    """
    <div style="
        text-align:center;
        color:#475569;
        font-size:11px;
        padding:8px 0 15px 0;
    ">
        Customer Feedback AI • Rule-Based Triage + Generative AI
    </div>
    """
)