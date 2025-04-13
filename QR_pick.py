import qrcode
import random
import string
import os
import json
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
OUTPUT_FOLDER = "Q더지_output"
NUM_QRS = 25
WINNER_INDEX = random.randint(0, NUM_QRS - 1)

def generate_key(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# 초기화
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
keys = {}
key_list = []

# QR 코드 생성
for i in range(NUM_QRS):
    key = generate_key()
    result = "win" if i == WINNER_INDEX else "lose"
    keys[key] = result
    key_list.append(key)

    qr_url = BASE_URL + "/check.html?key=" + key
    qr = qrcode.make(qr_url)
    qr.save(f"{OUTPUT_FOLDER}/qr_{i + 1}_{'win' if i == WINNER_INDEX else 'lose'}.png")

with open("public/keys.js", "w", encoding="utf-8") as f:
    f.write("const keys = ")
    json.dump(keys, f, indent=2)
    f.write(";")

print("=== Random Key Generated ===")
print(f"Winning Key: {list(keys.keys())[WINNER_INDEX]}")
print("=== Ready to deploy, check.html ===")
