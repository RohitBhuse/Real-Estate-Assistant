import re
import pandas as pd


# Query Understanding Functions

def parse_budget(text):

    text = text.lower().replace(",", "").strip()
    budget = None

    # crore 
    m = re.search(r'(\d+(\.\d+)?)\s*(cr|crore)', text)
    if m:
        budget = float(m.group(1)) * 100  # convert Cr → Lakh
    else:
        # lakh 
        m = re.search(r'(\d+(\.\d+)?)\s*(l|lac|lakh)', text)
        if m:
            budget = float(m.group(1))
    return budget


def parse_bhk(text):

    m = re.search(r'(\d+)\s*(bhk|bed|bedroom)', text.lower())
    if m:
        return int(m.group(1))
    return None


def parse_city(text, known_cities=None):
    if known_cities is None or len(known_cities) == 0:
        return None
    
    text_lower = text.lower()
    for city in known_cities:
        if isinstance(city, str) and city.lower() in text_lower:
            return city
    return None


def parse_landmark(text, known_landmarks=None):
    if known_landmarks is None or len(known_landmarks) == 0:
        return None
    
    text_lower = text.lower()
    for landmark in known_landmarks:
        if isinstance(landmark, str) and landmark.lower() in text_lower:
            return landmark
    return None



def parse_status(text):

    text = text.lower()
    if "ready" in text:
        return "Sell"
    elif "under construction" in text or "construction" in text:
        return "Not for Sale"
    return None


def extract_filters(user_text,known_cities=None,known_landmarks=None):

    city = parse_city(user_text, known_cities)
    landmark = parse_landmark(user_text, known_landmarks)
    bhk = parse_bhk(user_text)
    budget = parse_budget(user_text)
    status = parse_status(user_text)

    filters = {
        "city": city,
        "landmark": landmark,
        "bhk": bhk,
        "budget_lakh": budget,
        "status": status,
    }
    return {k: v for k, v in filters.items() if v is not None}



# Filtering the Data Function

def search_properties(df,filters):
    df_filtered = df.copy()

    if filters.get('city') and 'city' in df_filtered.columns:
        df_filtered = df_filtered[df_filtered['city'].str.lower() == filters['city'].strip().lower()]

    if filters.get('landmark') and 'landmark' in df_filtered.columns:
        df_filtered = df_filtered[df_filtered['landmark'].str.lower() == filters['landmark'].strip().lower()]

    if filters.get('bhk') is not None and 'type' in df_filtered.columns:
        df_filtered = df_filtered[df_filtered['type'] == filters['bhk']]

    if filters.get('budget_lakh') is not None and 'price' in df_filtered.columns:
        df_filtered = df_filtered[df_filtered['price'] <= filters['budget_lakh']]

    if filters.get('status') and 'listingType' in df_filtered.columns:
        df_filtered = df_filtered[df_filtered['listingType'].str.lower() == filters['status'].strip().lower()]

    return df_filtered



