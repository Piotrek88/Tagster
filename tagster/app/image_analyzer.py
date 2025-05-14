import boto3
import openai
from PIL import Image
import io
import os
import logging
import streamlit as st

logger = logging.getLogger(__name__)

# AWS credentials configuration at the beginning of the file
os.environ['AWS_ACCESS_KEY_ID'] = st.secrets["AWS_ACCESS_KEY_ID"]
os.environ['AWS_SECRET_ACCESS_KEY'] = st.secrets["AWS_SECRET_ACCESS_KEY"]
os.environ['AWS_DEFAULT_REGION'] = st.secrets["AWS_DEFAULT_REGION"]

def resize_image_to_limit(image, max_bytes=5*1024*1024):
    # Try to reduce the image size until it is below the limit
    quality = 90
    width, height = image.size
    while True:
        img_byte_arr = io.BytesIO()
        # Save as JPEG (smaller size than PNG)
        image.save(img_byte_arr, format='JPEG', quality=quality)
        img_bytes = img_byte_arr.getvalue()
        if len(img_bytes) <= max_bytes or quality < 30:
            return img_bytes
        # Reduce quality and resolution
        quality -= 10
        width = int(width * 0.9)
        height = int(height * 0.9)
        image = image.resize((width, height), Image.LANCZOS)

def analyze_image(image, only_description=False, custom_description=None):
    """
    Analizuje obraz i generuje jego opis oraz tagi.
    Args:
        image: Obraz w formacie PIL.Image
        only_description: jeśli True, zwraca tylko opis (tagi = None)
        custom_description: jeśli podano, generuje tagi na podstawie tego opisu
    Returns:
        tuple: (opis_zdjęcia, lista_tagów lub None)
    """
    try:
        # Automatic size reduction
        img_byte_arr = resize_image_to_limit(image)
        
        # Debug info
        st.write(f"Rozmiar obrazu: {len(img_byte_arr)} bajtów")
        st.write(f"Region AWS: {os.environ.get('AWS_DEFAULT_REGION')}")
             
        # Client initialization
        try:
            rekognition = boto3.client('rekognition', config=boto3.session.Config(proxies={}))
            st.write("Klient AWS został utworzony")
        except Exception as aws_init_error:
            st.error(f"Błąd podczas tworzenia klienta AWS: {str(aws_init_error)}")
            logger.error(f"AWS init error: {str(aws_init_error)}")
            return None, None

        # Connection test
        try:
            rekognition.list_collections()
            st.write("Połączenie z AWS działa poprawnie")
        except Exception as aws_error:
            st.error(f"Błąd połączenia z AWS: {str(aws_error)}")
            logger.error(f"AWS connection error: {str(aws_error)}")
            return None, None

        # Image analysis by AWS Rekognition
        response = rekognition.detect_labels(
            Image={'Bytes': img_byte_arr},
            MaxLabels=20,
            MinConfidence=80
        )

        # Download labels with their certainty
        labels = [(label['Name'], label['Confidence']) for label in response['Labels']]
        labels.sort(key=lambda x: x[1], reverse=True)

        # Preparing the context for GPT
        context = "Na zdjęciu wykryto następujące elementy:\n"
        for label, confidence in labels:
            context += f"- {label} (pewność: {confidence:.1f}%)"
            if 'Instances' in label and label['Instances']:
                context += f", liczba obiektów: {len(label['Instances'])}"
            context += "\n"

        num_persons = 0
        for label in response['Labels']:
            if label['Name'].lower() in ['person', 'child']:
                num_persons += len(label.get('Instances', []))
        context += f"\nLiczba wykrytych osób/dzieci: {num_persons}\n"

        client = openai.OpenAI(api_key=st.secrets['OPENAI_API_KEY'])

        if only_description:
            # Generate description only
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": """Jesteś ekspertem w opisywaniu zdjęć. Stwórz naturalny, płynny opis zdjęcia (maksymalnie 4 zdania). Nie wypisuj tagów ani dodatkowych informacji."""},
                    {"role": "user", "content": context}
                ]
            )
            description = response.choices[0].message.content
            return description, None

        if custom_description is not None:
            # Generate tags based on the given description
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": """Jesteś ekspertem w tagowaniu zdjęć. Wypisz NA KOŃCU tylko najważniejsze tagi (maksymalnie 5), oddzielone przecinkami, bez żadnych nagłówków, kropek, cudzysłowów ani dodatkowych znaków. Tagi mają być pojedynczymi słowami lub krótkimi frazami po polsku."""},
                    {"role": "user", "content": custom_description}
                ]
            )
            raw_tags = response.choices[0].message.content
            tags = [tag.strip().strip('.') for tag in raw_tags.split(',') if tag.strip()]
            return custom_description, tags

        # Default: description + tags
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": """Jesteś ekspertem w opisywaniu zdjęć. 
                Twoje zadanie to:
                1. Stworzyć naturalny, płynny opis zdjęcia (maksymalnie 4 zdania).
                2. Wypisz NA KOŃCU tylko najważniejsze tagi (maksymalnie 5), oddzielone przecinkami, bez żadnych nagłówków, kropek, cudzysłowów ani dodatkowych znaków. Tagi mają być pojedynczymi słowami lub krótkimi frazami po polsku.
                3. Nie opisuj ile czegoś jest na zdjęciu, tylko opisuj zdjęcie. 
                 Opis i tagi oddziel pustą linią (\\n\\n)."""},
                {"role": "user", "content": context}
            ]
        )
        full_response = response.choices[0].message.content
        description = full_response.split('\n\n')[0]
        raw_tags = full_response.split('\n\n')[1]
        tags = [tag.strip().strip('.') for tag in raw_tags.split(',') if tag.strip()]
        return description, tags
    except Exception as e:
        st.error(f"Szczegóły błędu: {str(e)}")
        logger.error(f"Błąd w analyze_image: {str(e)}")
        if "AccessDenied" in str(e) or "InvalidSignatureException" in str(e):
            raise Exception("Błąd konfiguracji AWS. Sprawdź ustawienia dostępu.")
        elif "InvalidImageFormat" in str(e):
            raise Exception("Nieprawidłowy format zdjęcia. Spróbuj użyć innego pliku.")
        else:
            raise Exception(f"Wystąpił błąd podczas analizy zdjęcia: {str(e)}")
