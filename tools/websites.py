import webbrowser

WEBSITES = {"youtube": "https://www.youtube.com", "github": "https://github.com",
            "gmail": "https://mail.google.com", "google": "https://www.google.com"}


def open_website(website: str) -> str:
    url = WEBSITES.get(website)
    if not url:
        raise RuntimeError("website is not approved")
    webbrowser.open(url)
    return f"Opened {website}."
