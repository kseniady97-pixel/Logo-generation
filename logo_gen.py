import requests
import random
import time
import base64
import os
import uuid
import logging
import config as cfg

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def generate_logo(forma, style, description, timeout=60):
    headers = {
        "Authorization": f"Bearer {cfg.IAM_TOKEN}",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    data = {
        "modelUri": f"art://{cfg.CATALOG_ID}/yandex-art/latest",
        "generationOptions": {
            "seed": str(random.randint(0, 1_000_000)),
            "aspectRatio": {"widthRatio": "1", "heightRatio": "1"}
        },
        "messages": [{
            "weight": "1",
            "text": f"Нарисуй логотип в форме {forma} под описание: {description}, в стиле: {style}"
        }]
    }

    try:
        response = requests.post(cfg.URL_1, headers=headers, json=data, timeout=15)
        response.raise_for_status()
        request_id = response.json().get("id")

        start = time.time()
        while time.time() - start < timeout:
            resp = requests.get(f"{cfg.URL_2}/{request_id}", headers={"Authorization": f"Bearer {cfg.IAM_TOKEN}"})
            if resp.status_code == 200 and "response" in resp.json():
                image_base64 = resp.json()["response"]["image"]
                image_data = base64.b64decode(image_base64)

                # Уникальное имя файла
                filename = f"{uuid.uuid4().hex}.jpeg"
                image_path = os.path.join("static", filename)
                with open(image_path, "wb") as f:
                    f.write(image_data)

                logging.info(f"Логотип сохранён: {image_path}")
                return {"success": True, "path": image_path}

            time.sleep(2)

        return {"success": False, "error": "Таймаут генерации изображения"}

    except Exception as e:
        logging.error(f"Ошибка генерации: {e}")
        return {"success": False, "error": str(e)}

print("IAM_TOKEN:", cfg.IAM_TOKEN)
print("CATALOG_ID:", cfg.CATALOG_ID)