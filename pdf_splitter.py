import streamlit as st
from pypdf import PdfReader, PdfWriter
from io import BytesIO

# Helper to parse custom page inputs like 1,3,5-7
def parse_pages(input_str):
    pages = set()
    for part in input_str.split(','):
        if '-' in part:
            start, end = map(int, part.split('-'))
            pages.update(range(start - 1, end))
        else:
            pages.add(int(part.strip()) - 1)
    return sorted(pages)

# Streamlit app UI
st.set_page_config(page_title="PDF Page Extractor", layout="centered")
st.title("📄 Extract Specific Pages from a PDF")

uploaded_file = st.file_uploader("Upload PDF", type="pdf")

if uploaded_file:
    try:
        reader = PdfReader(uploaded_file)
        total_pages = len(reader.pages)
        st.success(f"PDF uploaded successfully. Total pages: {total_pages}")

        page_input = st.text_input("Enter page numbers (e.g., 1,3,5-7):")

        if st.button("Extract"):
            selected_pages = parse_pages(page_input)
            writer = PdfWriter()

            for i in selected_pages:
                if 0 <= i < total_pages:
                    writer.add_page(reader.pages[i])
                else:
                    st.warning(f"Page {i+1} is out of range.")

            output = BytesIO()
            writer.write(output)
            output.seek(0)

            st.download_button(
                label="📥 Download Extracted PDF",
                data=output,
                file_name="selected_pages.pdf",
                mime="application/pdf"
            )
    except Exception as e:
        st.error(f"An error occurred: {e}")
