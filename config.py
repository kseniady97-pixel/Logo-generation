import os
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

IAM_TOKEN = os.getenv("IAM_TOKEN")
CATALOG_ID = os.getenv("CATALOG_ID")
URL_1 = "https://llm.api.cloud.yandex.net/foundationModels/v1/imageGenerationAsync"
URL_2 = "https://llm.api.cloud.yandex.net:443/operations"