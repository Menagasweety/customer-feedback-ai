# ✦ Customer Feedback AI Assistant

A modern, hands-on customer-feedback triage and response-drafting application for an electronics retailer.

The app combines:

- Python + Pandas for data handling
- Transparent rule-based Critical feedback detection
- Keyword-based complaint guidance
- Gemini for short, empathetic response drafts
- Human editing and revision before any manual sending

**No machine-learning classifier is used. The app does not send emails automatically.**

## What the app demonstrates

```text
Electronics Reviews
       ↓
Pandas Data Loading
       ↓
1–2 Star → Critical
       ↓
Complaint Keyword Analysis
       ↓
Select / Enter Customer Feedback
       ↓
Gemini API
       ↓
AI Email Draft
       ↓
Human Edit / Revision
       ↓
Copy Response
```

## UI

### Dashboard
Shows total reviews, Critical reviews, Critical rate, average rating, rating distribution, and top complaint categories.

### Existing Feedback
Search and filter the included 3,600-review electronics dataset. Select a review and generate a response draft.

### Write Your Own Review
Enter your own product name, 1–5 star rating, and review. The app classifies 1–2 stars as Critical and uses the same complaint dictionary for guidance. Then click **Generate My Response Email**.

### AI Response
The generated email appears in an editable block. You can edit it, copy it, or request a revised draft using additional reviewer instructions.

### API Session
The Gemini API key is entered by the user only when needed. It is kept in Streamlit session state, is not displayed back, and is not written to the project files. The sidebar includes **Delete API Key from Session** to clear it from the current app session.

> Deleting the key from the app session does not revoke/delete the key from Google's account. It only removes the copy held by this running application session.

## Dataset

The included `data/reviews.csv` is the electronics review dataset used in the capstone workflow.

Source: Mendeley Data, **Sentiment in Customer Reviews**, Version 1, DOI `10.17632/2zfbcy96vp.1`.

Source page: https://data.mendeley.com/datasets/2zfbcy96vp/1

The dataset contains 3,600 customer reviews. The project previously identified 687 Critical reviews using the 1–2 star rule.

## Run locally on Windows

### 1. Install Python

Install Python 3.10+ if it is not already installed.

### 2. Open the project folder

Open the extracted project folder in VS Code.

### 3. Open the VS Code terminal

Use:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can run the app without activating the environment after installing packages with:

```powershell
py -m pip install -r requirements.txt
```

### 4. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 5. Start the app

```powershell
python -m streamlit run app.py
```

A browser window should open with the application.

## Gemini API key

You can create a Gemini API key through Google AI Studio.

Do not put the key in:

- `app.py`
- `README.md`
- GitHub
- the dataset
- screenshots
- `.env` committed to GitHub

The app asks for the key at runtime through a password-style input.

The app intentionally does not persist the entered key to disk.

## GitHub upload — easiest method

### Step 1 — Create a GitHub account

Go to GitHub and sign in.

### Step 2 — Create a new repository

Click **New repository**.

Suggested name:

```text
customer-feedback-ai-assistant
```

Choose **Public** if you want recruiters/evaluators to view it.

Do not add another README during repository creation because this project already contains one.

### Step 3 — Upload the project

On the new repository page:

1. Click **Add file**.
2. Click **Upload files**.
3. Upload the contents of this project folder.
4. Make sure `app.py`, `requirements.txt`, `README.md`, `src/`, and `data/` are present.
5. Scroll down.
6. Enter a commit message such as:

```text
Initial customer feedback AI assistant
```

7. Click **Commit changes**.

### Step 4 — Check the repository

Your GitHub repository should look like:

```text
customer-feedback-ai-assistant/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── data/
│   └── reviews.csv
└── src/
    ├── __init__.py
    ├── data_processing.py
    ├── complaint_analysis.py
    └── gemini_response.py
```

## GitHub safety check before publishing

Before making the repository public, search the repository for strings such as:

```text
AIza
GEMINI_API_KEY
api_key =
```

There should be **no real API key** in the repository.

The application asks for the key at runtime instead.

## Optional: run from GitHub after upload

If you later deploy the app on Streamlit Community Cloud:

1. Sign in to Streamlit Community Cloud.
2. Connect your GitHub account.
3. Select this repository.
4. Select `app.py` as the main file.
5. Deploy.

For this project, the user-facing app still asks for the Gemini API key at runtime rather than committing a key to GitHub.

## Important project boundaries

This GitHub version intentionally does **not** add:

- Machine-learning classification
- Automatic email sending
- Customer login/authentication
- CRM integration
- Database infrastructure
- Refund/replacement automation

Those are outside the current assessment workflow.

## Security limitation to understand

The API key is not stored by this application in a file or Git repository and is cleared by the **Delete API Key from Session** button. However, no software can honestly promise that a secret entered into a third-party hosted server is invisible to the server operator. For a personal/local run, the key stays in the running app's session memory.

## Project statement

> This application demonstrates a transparent, rule-based customer-feedback triage workflow and uses Generative AI only for response drafting. The final response remains under human control.

This is live :https://customer-feedback-ai-478ierzsten73mhcms3fpf.streamlit.app/
