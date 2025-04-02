from flask import Flask, render_template, request
import pandas as pd
import requests
import os  # ← 포트 번호 읽기 위해 추가

app = Flask(__name__)

KAKAO_API_KEY = "d91284b17eec953bd5d9002ea891c02d"  # ← 본인 키

def geocode(address):
    url = "https://dapi.kakao.com/v2/local/search/address.json"
    headers = {"Authorization": f"KakaoAK {KAKAO_API_KEY}"}
    params = {"query": address}
    res = requests.get(url, headers=headers, params=params)
    try:
        doc = res.json()["documents"][0]
        return doc["y"], doc["x"]
    except:
        return None, None

@app.route("/", methods=["GET", "POST"])
def index():
    locations = []
    if request.method == "POST":
        file = request.files["file"]
        if file:
            df = pd.read_excel(file)
            for _, row in df.iterrows():
                name = row.get("이름", "")
                address = row.get("주소", "")
                lat, lng = geocode(address)
                print("📍 변환된 주소:", name, address, lat, lng)
                if lat and lng:
                    locations.append({
                        "name": name,
                        "address": address,
                        "lat": lat,
                        "lng": lng
                    })
    return render_template("map.html", locations=locations)

# ✅ Render 배포용 실행 방식
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render에서 지정한 포트 사용
    app.run(host="0.0.0.0", port=port)
