# GitHub Upload — Beginner Guide

## A. Extract the ZIP

Extract the project ZIP to a normal folder, for example:

```text
Desktop/customer-feedback-ai-assistant/
```

Open that folder in VS Code.

## B. Test it before GitHub

Open VS Code Terminal and run:

```powershell
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

The browser should open.

Try the **Write Your Own Review** tab. Enter a product, stars, and a review. When you click Generate, the app will ask for the Gemini API key in the sidebar.

## C. Create GitHub repository

1. Open GitHub.
2. Click **+** → **New repository**.
3. Repository name: `customer-feedback-ai-assistant`
4. Choose Public or Private.
5. Do not add another README.
6. Click **Create repository**.

## D. Upload using the browser — easiest

1. Open your empty GitHub repository.
2. Click **Add file**.
3. Click **Upload files**.
4. Drag the project files/folders into the upload area.
5. Confirm the files are visible.
6. Add commit message:

```text
Initial customer feedback AI assistant
```

7. Click **Commit changes**.

## E. Never upload the API key

The key should only be typed into the running application.

Never paste it into:

- `app.py`
- `README.md`
- GitHub
- `.gitignore`
- screenshots
- chat messages

## F. If you accidentally expose a key

Do not just delete the line and assume the secret is gone: Git history may still contain it. Revoke/rotate the exposed key in the provider's console, then remove the secret from the repository history if necessary.
