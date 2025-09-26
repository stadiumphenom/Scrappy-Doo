import streamlit as st
import subprocess
import sys

# Safe import of BeautifulSoup
try:
    from bs4 import BeautifulSoup
except ModuleNotFoundError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "beautifulsoup4"])
    from bs4 import BeautifulSoup

from scrapling.engines.static import StealthyFetcher
from scrapling.engines.toolbelt.custom import Response


def extract_structured_data(html: str) -> dict:
    """Parses HTML and returns structured content."""
    soup = BeautifulSoup(html, "html.parser")

    return {
        "title": soup.title.string.strip() if soup.title else "No title",
        "headings": [h.get_text(strip=True) for h in soup.find_all(["h1", "h2"])],
        "links": [
            {"text": a.get_text(strip=True), "href": a.get("href")}
            for a in soup.find_all("a", href=True)
        ],
        "meta": {
            tag.get("name") or tag.get("property"): tag.get("content")
            for tag in soup.find_all("meta", attrs={"content": True})
            if tag.get("name") or tag.get("property")
        },
    }


def main():
    st.set_page_config(page_title="Scrappy-Doo", layout="centered")
    st.title("🦴 Scrappy‑Doo Structured Scraper")

    url = st.text_input("Enter a URL to fetch")
    headless = st.checkbox("Run Headless", value=True)
    network_idle = st.checkbox("Wait for Network Idle", value=False)
    load_dom = st.checkbox("Load Full DOM", value=True)

    if st.button("Fetch & Parse"):
        if not url:
            st.warning("Please enter a URL.")
            return

        with st.spinner("Fetching and parsing..."):
            try:
                response: Response = StealthyFetcher.fetch(
                    url=url,
                    headless=headless,
                    network_idle=network_idle,
                    load_dom=load_dom,
                )

                html = response.text
                structured = extract_structured_data(html)

                st.success("✅ Success! Here’s the structured data:")

                st.subheader("📝 Title")
                st.text(structured["title"])

                st.subheader("🔗 Links")
                for link in structured["links"][:10]:  # limit to 10
                    st.markdown(f"- [{link['text'] or '(no text)'}]({link['href']})")

                st.subheader("📣 Headings")
                for h in structured["headings"]:
                    st.write("•", h)

                st.subheader("🧠 Meta Tags")
                st.json(structured["meta"])

                # Optional: download raw HTML
                st.download_button("Download HTML", html, file_name="scraped_page.html")

            except Exception as e:
                st.error(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
