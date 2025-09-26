import streamlit as st
import pandas as pd

from engines import fetchers

st.set_page_config(page_title="Scrappy-Doo", layout="wide")

def main():
    st.title("🦴 Scrappy-Doo Streamlit UI")

    st.markdown("Scrape and view results directly from this dashboard.")

    # Input for scraping
    st.subheader("🔍 Enter a Target to Scrape")
    target = st.text_input("Target URL or keyword")

    if st.button("Start Scraping"):
        with st.spinner("Fetching data..."):
            try:
                # Hypothetical function — update to match fetchers.py
                result = fetchers.fetch(target)  # Or fetchers.run(), etc.
                st.success("Scraping completed!")

                if isinstance(result, dict):
                    st.json(result)
                elif isinstance(result, pd.DataFrame):
                    st.dataframe(result)
                else:
                    st.write(result)
            except Exception as e:
                st.error(f"Error: {e}")

    st.markdown("---")

    # Load from storage (optional)
    st.subheader("📂 Load Stored Results")
    if st.button("Load Latest"):
        try:
            from core import storage
            data = storage.load_latest()  # Hypothetical
            if isinstance(data, pd.DataFrame):
                st.dataframe(data)
            else:
                st.write(data)
        except Exception as e:
            st.error(f"Could not load: {e}")

if __name__ == "__main__":
    main()
