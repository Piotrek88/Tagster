#!/bin/bash

# Przejdź do katalogu aplikacji (jeśli trzeba)
cd /workspace

# Utwórz katalog .streamlit, jeśli nie istnieje
mkdir -p .streamlit

# Uruchom skrypt generujący sekrety
python tagster/app/generate_secrets.py

# Uruchom aplikację Streamlit
streamlit run tagster/app/main.py