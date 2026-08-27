# 현장 인원 배치판

창고 배치 이미지를 배경으로 고정하고 작업자 이름표를 드래그해 각 작업 구역에 배치하는 Streamlit 앱입니다.

## 실행

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

## 포함 기능

- 작업자 이름표 드래그·드롭
- 배치 위치에 따른 구역 자동 판정
- 현장·사무실·휴무·미배치 자동 집계
- 날짜별 브라우저 저장
- 전일 배치 불러오기
- 작업자 추가 및 삭제
- 구역 판정선 표시
- JSON 백업 다운로드
- PC 및 태블릿 화면 대응

## 저장 방식

현재 초안은 브라우저 `localStorage`에 저장합니다. 같은 PC와 같은 브라우저에서는 날짜별 배치가 유지됩니다. 여러 PC가 같은 배치를 공유하려면 다음 단계에서 Supabase, PostgreSQL 또는 사내 데이터베이스를 연결해야 합니다.

## GitHub 배포

저장소 루트에 이 폴더의 파일을 넣고 Streamlit Community Cloud에서 `app.py`를 시작 파일로 선택합니다.

