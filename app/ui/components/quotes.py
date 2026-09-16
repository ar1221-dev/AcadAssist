"""Motivational quotes configuration for AcadAssist.

Strict Rule: Only ONE prominent quote per page (rendered in the sidebar bottom
or the designated page milestone).
"""

PAGE_QUOTES = {
    "Dashboard": "DISCIPLINE TURNS GOALS INTO RESULTS.",
    "My Knowledge": "Good students build knowledge. Great ones organize it.",
    "Assessment": "Consistent practice builds confidence.",
    "Study Planner": "A well planned day brings a calmer tomorrow.",
    "AI Study Assistant": "Better questions lead to deeper understanding.",
    "Progress": "Progress today, possibilities tomorrow.",
    "Settings": "A better learning experience is a choice you make today.",
    "Help & Support": "Support today, a stronger you tomorrow.",
    "Profile": "A better version of you is always a work in progress.",
}


def get_quote_for_page(page_name: str) -> str:
    """Retrieve the single canonical quote for the active page."""
    return PAGE_QUOTES.get(page_name, "Small steps today lead to big results tomorrow.")
