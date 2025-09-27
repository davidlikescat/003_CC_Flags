# Canva 국기 퀴즈 영상 제작 가이드

## 📁 파일 구조
```
canva_upload_ready/
├── csv_data/
│   └── flag_quiz_data.csv          # 퀴즈 데이터 (255개)
├── flag_images/
│   └── svg/
│       ├── beginner/              # 쉬움 (85개)
│       ├── intermediate/          # 보통 (85개)
│       └── high/                  # 어려움 (85개)
└── documentation/
    ├── canva_usage_guide.md       # 이 파일
    └── csv_structure.md           # CSV 구조 설명
```

## 🎬 Canva에서 Bulk Create 사용법

### 1단계: 템플릿 준비
1. Canva Pro 계정으로 로그인
2. "Create a design" → "Custom size" → 1080x1920 (세로형) 또는 1920x1080 (가로형)
3. 15초 영상 템플릿 생성:
   - 배경 설정
   - 국기 이미지 영역 추가
   - 질문 텍스트: "Which country does this flag belong to?"
   - 4개 선택지 (A, B, C, D) 영역 생성

### 2단계: Bulk Create 설정
1. 왼쪽 메뉴에서 "Apps" → "Bulk Create" 검색 및 설치
2. "Connect your data" 클릭
3. `csv_data/flag_quiz_data.csv` 파일 업로드

### 3단계: 데이터 연결
템플릿의 각 요소를 CSV 컬럼과 연결:
- 국기 이미지 → `flag_image_path` 컬럼 (예: beginner/beginner01.svg)
- 질문 텍스트 → `question_text` 컬럼
- 선택지 A → `option_a` 컬럼
- 선택지 B → `option_b` 컬럼
- 선택지 C → `option_c` 컬럼
- 선택지 D → `option_d` 컬럼
- 난이도 표시 → `difficulty_number` 컬럼 (예: beginner01, intermediate01, high01)

### 4단계: 생성 및 다운로드
1. "Generate designs" 클릭 → 255개 영상 자동 생성
2. "Download all" → MP4 형식으로 일괄 다운로드

## 📊 CSV 데이터 구조

| 컬럼명 | 설명 | 예시 |
|--------|------|------|
| quiz_id | 퀴즈 번호 | 1, 2, 3... |
| difficulty | 난이도 | beginner, intermediate, high |
| difficulty_number | 난이도별 순차 번호 | beginner01, intermediate01, high01 |
| country_filename | 원본 파일명 | korea, united_states |
| country_name | 정답 국가명 | Korea, United States |
| flag_image_path | 국기 이미지 경로 | beginner/beginner01.svg |
| question_text | 질문 | Which country does this flag belong to? |
| option_a~d | 선택지 | Korea, Japan, China, Thailand |
| correct_answer | 정답 | Korea |
| correct_option | 정답 선택지 | A, B, C, D |

## 🎯 난이도별 특징

### 🟢 Beginner (85개)
- 주요 강대국 (미국, 중국, 일본, 독일 등)
- 올림픽 강국
- 독특한 디자인으로 유명한 국기

### 🟡 Intermediate (85개)
- 중견국가
- 지역적으로 유명한 국가
- 특별한 역사적 의미가 있는 국가

### 🔴 High (85개)
- 작은 섬나라
- 인지도가 낮은 국가
- 특별 행정구역

## 💡 팁
- 각 영상은 15초로 설정 권장
- 정답 공개 타이밍: 10-12초 후
- 배경음악 추가로 몰입도 향상
- 썸네일에 국기 일부를 보여주어 호기심 유발

## 🚀 최적화 제안
- 배치별 제작: 난이도별로 나누어 제작
- A/B 테스트: 다른 템플릿으로 성과 비교
- 시리즈화: "세계 국기 퀴즈 시리즈"로 브랜딩
