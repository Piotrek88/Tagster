import streamlit as st
import os
from PIL import Image
import logging
from image_analyzer import analyze_image
from faq_handler import get_faq_answer
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, '..', 'data')
LOG_PATH = os.path.join(DATA_DIR, 'app.log')

# Logger configuration
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)
logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(message)s'
)

print("HTTP_PROXY:", os.environ.get("HTTP_PROXY"))
print("HTTPS_PROXY:", os.environ.get("HTTPS_PROXY"))

st.markdown(
    "<h1 style='text-align: center; color: red; font-size: 70px;'>Tagster</h1>",
    unsafe_allow_html=True
)

MAX_FILE_SIZE_MB = 5
MAX_PIXELS = 15_000_000  # 15 megapixels

# Image analysis section
st.header("Analiza Obrazu")
uploaded_file = st.file_uploader("Wybierz zdjęcie", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Przesłane zdjęcie", use_column_width=True)
    if st.button("Analizuj zdjęcie"):
        with st.spinner("Analizuję zdjęcie..."):
            try:
                description, _ = analyze_image(image, only_description=True)
                st.session_state['description'] = description
                st.session_state['tags'] = None
            except Exception as e:
                st.error("Wystąpił błąd podczas analizy zdjęcia. Spróbuj ponownie lub użyj innego zdjęcia.")
                logging.error(f"Błąd analizy zdjęcia: {e}")

    if 'description' in st.session_state and st.session_state['description']:
        st.subheader("Opis zdjęcia:")
        edited_description = st.text_area("Możesz poprawić opis poniżej:", value=st.session_state['description'], height=120, key="desc_edit")
        if st.button("Akceptuję opis i generuj tagi"):
            with st.spinner("Generuję tagi na podstawie opisu..."):
                try:
                    # Generate tags based on accepted description
                    _, tags = analyze_image(image, custom_description=edited_description)
                    st.session_state['tags'] = tags
                    st.session_state['description'] = edited_description
                except Exception as e:
                    st.error("Wystąpił błąd podczas generowania tagów. Spróbuj ponownie.")
                    logging.error(f"Błąd generowania tagów: {e}")
        
        if st.session_state.get('tags'):
            st.subheader("Tagi:")
            tag_cols = st.columns(5)
            for i, tag in enumerate(st.session_state['tags']):
                with tag_cols[i % 5]:
                    st.markdown(
                        f"<div style='background-color: white; padding: 5px 10px; border-radius: 15px; text-align: center; color: black; font-weight: bold;'>{tag}</div>",
                        unsafe_allow_html=True
                    )

st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)
# FAQ section
st.header("FAQ")
question = st.text_input("Zadaj pytanie:")

# Check if the question contains allowed characters
def is_valid_question(q):
    # Remove whitespace and punctuation
    cleaned = re.sub(r'[\s\W_]+', '', q, flags=re.UNICODE)
    return len(cleaned) > 0

if question:
    if not is_valid_question(question):
        st.warning("Pytanie musi zawierać litery...")
    else:
        # Automatically send the query on Enter
        answer = get_faq_answer(question)
        st.write(answer)
