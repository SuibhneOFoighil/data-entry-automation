import random
import json
import streamlit as st
import pandas as pd
import extract as ex
from tempfile import NamedTemporaryFile
from dotenv import load_dotenv

load_dotenv()

# 5. Streamlit app
def main():

    if 'db' not in st.session_state:
        default_data_points = {
            "Spring Classes Begin": "The date when classes begin for the spring semester",
            "Spring Break": "The date when spring break begins",
            "Spring Classes End": "The date when classes end for the spring semester",
        }
        st.session_state.db = pd.DataFrame(default_data_points.items(), columns=["Field", "Description"])

    db = st.session_state.db

    st.set_page_config(page_title="Doc extraction", page_icon=":bird:")

    st.header("Doc extraction :bird:")

    uploaded_files = st.file_uploader("upload PDFs", accept_multiple_files=True)
    db_spot = st.empty()
    editor = db_spot.data_editor(db, num_rows="dynamic", hide_index=True)

    data_points = dict(zip(editor["Field"], editor["Description"]))

    if st.button("Extract") and uploaded_files is not None and data_points is not None:
        results = []
        for file in uploaded_files:
            with NamedTemporaryFile(dir='.', suffix='.csv') as f:
                f.write(file.getbuffer())
                content = ex.extract_content_from_url(f.name)
                data = ex.extract_structured_data(content, data_points)
                print(data)
                json_data = json.loads(data)
                if isinstance(json_data, list):
                    results.extend(json_data)  # Use extend() for lists
                else:
                    results.append(json_data)  # Wrap the dict in a list

        if len(results) > 0:
            try:
                st.success("Extraction successful!")
                st.write(results)
            except Exception as e:
                st.error(
                    f"An error occurred while creating the DataFrame: {e}")
                st.write(results)  # Print the data to see its content

if __name__ == '__main__':
    main()