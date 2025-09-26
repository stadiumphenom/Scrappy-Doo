import streamlit as st
from scrapling.engines.static import StealthyFetcher
from scrapling.engines.toolbelt.custom import Response


def main():
    st.set_page_config(page_title="Scrappy-Doo", layout="centered")
    st.title("🦴 Scrappy‑Doo Basic Scraper")

    st.markdown("This tool fetches and displays raw HTML content using Scrapling.")

    url = st.text_input("Enter a URL to fetch")
    headless = st.checkbox("Run Headless", value=True)
    network_idle = st.checkbox("Wait for Network Idle", value=False)
    load_dom = st.checkbox("Load Full DOM", value=True)

    if st.button("Fetch Page"):
        if not url:
            st.warning("Please enter a URL.")
            return

        with st.spinner("Fetching..."):
            try:
                response: Response = StealthyFetcher.fetch(
                    url=url,
                    headless=headless,
                    network_idle=network_idle,
                    load_dom=load_dom,
                )

                html = response.text

                st.success("✅ Page fetched successfully!")

                st.subheader("🧾 Raw HTML (first 5,000 chars)")
                st.code(html[:5000], language="html")

                st.download_button("Download Full HTML", html, file_name="scraped_page.html")

            except Exception as e:
                st.error(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
