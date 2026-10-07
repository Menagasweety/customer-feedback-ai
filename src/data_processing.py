from pathlib import Path
import pandas as pd


# ---------------------------------------------------------
# DATASET PATH
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "reviews.csv"


# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

def load_data():
    """
    Load the customer reviews dataset from data/reviews.csv.
    """

    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found at: {DATA_PATH}\n"
            "Make sure the file exists at data/reviews.csv"
        )

    df = pd.read_csv(DATA_PATH)

    # Standardize column names
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    # Convert stars to numeric
    if "stars" in df.columns:
        df["stars"] = pd.to_numeric(df["stars"], errors="coerce")

    # Make review text safe for analysis
    if "comments" in df.columns:
        df["comments"] = df["comments"].fillna("").astype(str)

    # Create critical flag using the project rule
    if "stars" in df.columns:
        df["critical"] = df["stars"] <= 2
    else:
        df["critical"] = False

    return df


# ---------------------------------------------------------
# DASHBOARD METRICS
# ---------------------------------------------------------

def get_dashboard_metrics(df):
    """
    Calculate the main dashboard metrics.
    """

    total_reviews = len(df)

    if "critical" in df.columns:
        critical_reviews = int(df["critical"].sum())
    elif "stars" in df.columns:
        critical_reviews = int((df["stars"] <= 2).sum())
    else:
        critical_reviews = 0

    if total_reviews > 0:
        critical_percentage = (
            critical_reviews / total_reviews
        ) * 100
    else:
        critical_percentage = 0

    if "stars" in df.columns:
        average_rating = df["stars"].mean()
    else:
        average_rating = 0

    return {
        "total_reviews": total_reviews,
        "critical_reviews": critical_reviews,
        "critical_percentage": critical_percentage,
        "average_rating": average_rating,
    }