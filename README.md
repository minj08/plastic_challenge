🧠 Plastic Challenge
플라스틱 절감 행동을 기록하고 시각화하는 웹 애플리케이션입니다. 
사용자는 플라스틱 절감 행동을 인증 이미지로 업로드하고, 기록은 통계로 시각화되며, 인증 이미지는 갤러리로 제공됩니다.

🚀 주요 기능
✅ 이미지 업로드	사용자가 행동을 선택하고 인증 이미지를 업로드
✅ 포인트 계산	절감량(g)을 기반으로 포인트 자동 계산 
✅ 사용자 관리	사용자 생성 및 포인트 조회 기능
✅ 통계 시각화	날짜별 절감량을 Chart.js로 시각화 (/stats)
✅ 이미지 갤러리	업로드된 인증 이미지를 /gallery에서 확인 가능

🖥️ 웹 화면 구성

/	홈 화면
/record	플라스틱 절감 행동 기록 화면 (이미지 업로드)
/stats	날짜별 절감량 통계 시각화
/gallery	인증 이미지 갤러리
/user/<id>	사용자 정보 조회 API
/upload	이미지 업로드 API
/user_stats	통계 데이터 API (JSON)

📦 설치 방법
bash

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

🧪 테스트 방법
브라우저에서 http://127.0.0.1:5050/record 접속

사용자 ID 입력 → 행동 선택 → 이미지 업로드

JSON 응답 확인 → /gallery에서 이미지 표시

/stats에서 날짜별 절감량 확인

📁 폴더 구조
plastic_challenge/
├── app.py
├── data.db
├── uploads/              # 업로드된 이미지 저장
├── templates/
│   ├── home.html
│   ├── record.html
│   ├── stats.html
│   └── gallery.html
├── static/               # (필요 시) CSS, JS 파일
├── requirements.txt
└── README.md

📌 주의사항
uploads/, data.db는 .gitignore에 포함되어 GitHub에 올라가지 않습니다
이미지 분류 기능은 향후 머신러닝 모델을 통해 구현 예정입니다
Flask 서버는 기본 포트 5050에서 실행됩니다

🧠 향후 개선 아이디어
이미지 분류 모델 연동 (TensorFlow 또는 PyTorch)
사용자별 랭킹 시스템
월별 절감량 통계

배지 시스템 및 알림 기능

모바일 대응 UI
