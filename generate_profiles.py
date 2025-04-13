import os
import pandas as pd
import qrcode
from jinja2 import Environment, FileSystemLoader
from dotenv import load_dotenv
load_dotenv()

CSV_FILE = 'input_data.csv'
TEMPLATE_FILE = 'profile_demo.html'

BASE_URL = os.getenv("BASE_URL")

OUTPUT_FOLDER = 'generated_profiles'
QR_FOLDER = 'generated_qrcodes'

def generate_html(data_dict):
    env = Environment(loader=FileSystemLoader(searchpath="./"))
    template = env.get_template(TEMPLATE_FILE)
    return template.render(data_dict)

# HTML 저장
def save_html(file_name, content):
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)
    file_path = os.path.join(OUTPUT_FOLDER, file_name)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"=== Saved HTML: {file_path}")
    return file_path

def generate_qr(filename):
    if not os.path.exists(QR_FOLDER):
        os.makedirs(QR_FOLDER)
    profile_url = BASE_URL + filename
    qr = qrcode.make(profile_url)
    qr_path = os.path.join(QR_FOLDER, f"{os.path.splitext(filename)[0]}_qrcode.png")
    qr.save(qr_path)
    print(f"QR Generated: {qr_path} → {profile_url}")

def main():
    df = pd.read_csv(CSV_FILE)

    for idx, row in df.iterrows():
        profile_data = {
            '국문이름': row['국문이름'],
            '영문이름': row['영문이름'],
            '학교': row['학교'],
            '이메일': row['이메일'],
            '직무': row['직무'],
            '관심키워드1': row['관심키워드1 - hashtag1'],
            '관심키워드2': row['관심키워드2 - hashtag2'],
            '관심키워드3': row['관심키워드3 - hashtag3'],
            '경력1': row['경력 1'],
            '경력2': row['경력 2'],
            '경력3': row['경력 3'],
            '링크드인': row['LinkedIn 링크 (Only if you have)'],
            '프로필사진': row['프로필 사진'],
            '학과': row['학과']
        }

        file_name = f"{row['영문이름'].replace(' ', '_')}.html"
        html_content = generate_html(profile_data)
        save_html(file_name, html_content)
        generate_qr(file_name)

    print("\n ==== All profiles and QR codes have been successfully generated! ====")

if __name__ == "__main__":
    main()
