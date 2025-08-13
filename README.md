# 🧠 Plastic Challenge

**플라스틱 분류기 프로젝트입니다.**  
이 프로젝트는 머신러닝 모델을 활용해 다양한 플라스틱 종류를 자동으로 분류합니다.  
사용자는 이미지를 업로드하면, 모델이 해당 플라스틱의 종류를 예측해줍니다.

---

## 🚀 주요 기능

- 이미지 업로드를 통한 플라스틱 분류
- TensorFlow 기반 사전 학습된 모델 사용
- Flask 웹 서버로 간편한 API 제공
- 향후 웹 UI 확장 가능

---

## 📦 설치 방법

```bash
# 1. 저장소 클론
git clone https://github.com/minj08/plastic_challenge.git
cd plastic_challenge

# 2. 가상환경 생성 (선택)
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 3. 필수 패키지 설치
pip install -r requirements.txt

# 4. 서버 실행
python app.py
