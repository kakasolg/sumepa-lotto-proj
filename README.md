uv init
uv venv --python 3.12 .venv
uv add flask

# 방법 1: Flask CLI 사용 (권장)
flask run

# 방법 2: Python으로 직접 실행
python app.py

# 방법 2: 디버그 모드 실행
set FLASK_ENV=development
set FLASK_DEBUG=1
flask run