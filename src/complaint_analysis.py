import re
from collections import Counter


# ---------------------------------------------------------
# COMPLAINT DICTIONARY
# ---------------------------------------------------------

COMPLAINT_DICTIONARY = {
    "battery": [
        "battery",
        "battery life",
        "battery backup",
        "drains",
        "drain",
        "backup"
    ],

    "charging": [
        "charge",
        "charging",
        "charger",
        "charging port",
        "slow charge",
        "fast charge"
    ],

    "heating": [
        "heat",
        "heating",
        "overheat",
        "overheating",
        "hot"
    ],

    "camera": [
        "camera",
        "photo",
        "picture",
        "pictures",
        "image",
        "images",
        "flash"
    ],

    "display": [
        "screen",
        "display",
        "brightness",
        "touchscreen",
        "touch screen",
        "pixels"
    ],

    "audio": [
        "sound",
        "speaker",
        "speakers",
        "volume",
        "audio",
        "headphone",
        "earphone"
    ],

    "connectivity": [
        "wifi",
        "wi fi",
        "bluetooth",
        "network",
        "signal",
        "connection",
        "connect"
    ],

    "software": [
        "software",
        "app",
        "apps",
        "android",
        "update",
        "lag",
        "lags",
        "slow",
        "crash",
        "hang"
    ],

    "quality_or_damage": [
        "broken",
        "defect",
        "defective",
        "poor quality",
        "cheap quality",
        "damaged",
        "damage",
        "faulty",
        "stopped working",
        "not working"
    ],

    "delivery_or_packaging": [
        "delivery",
        "delivered",
        "package",
        "packaging",
        "box",
        "shipping",
        "late",
        "missing item"
    ],

    "value_or_expectation": [
        "price",
        "expensive",
        "worth",
        "waste",
        "disappointed",
        "expect",
        "expectation"
    ],
}


# ---------------------------------------------------------
# GET CRITICAL REVIEWS
# ---------------------------------------------------------

def get_critical_reviews(df):
    """
    Rule-based filtering:
    Reviews with ratings of 1 or 2 stars are considered critical.
    """

    critical_df = df[df["stars"] <= 2].copy()

    return critical_df


# ---------------------------------------------------------
# FIND COMPLAINT CATEGORIES FOR ONE REVIEW
# ---------------------------------------------------------

def find_complaint_categories(review_text):
    """
    Identify complaint categories using keyword matching.
    """

    text = str(review_text).lower()

    matched_categories = []

    for category, keywords in COMPLAINT_DICTIONARY.items():

        for keyword in keywords:

            # Case-insensitive keyword search
            if re.search(r"\b" + re.escape(keyword) + r"\b", text):
                matched_categories.append(category)
                break

    return matched_categories


# ---------------------------------------------------------
# ANALYZE COMPLAINTS
# ---------------------------------------------------------

def analyze_complaints(df):
    """
    Analyze complaint categories across critical reviews.

    Returns:
        critical_reviews
        complaint_counts
        analyzed_reviews
    """

    critical_reviews = get_critical_reviews(df)

    complaint_counter = Counter()
    analyzed_reviews = critical_reviews.copy()

    analyzed_reviews["complaint_categories"] = (
        analyzed_reviews["comments"]
        .apply(find_complaint_categories)
    )

    analyzed_reviews["complaint_category_count"] = (
        analyzed_reviews["complaint_categories"]
        .apply(len)
    )

    for categories in analyzed_reviews["complaint_categories"]:
        complaint_counter.update(categories)

    return (
        critical_reviews,
        complaint_counter,
        analyzed_reviews
    )