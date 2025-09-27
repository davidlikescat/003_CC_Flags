# CSV 데이터 구조 상세 설명

## 컬럼별 설명

### 기본 정보
- `quiz_id`: 퀴즈 고유 번호 (1-255)
- `difficulty`: 난이도 레벨 (beginner/intermediate/high)
- `country_filename`: 파일명용 국가명 (소문자, 언더스코어)
- `country_name`: 표시용 정식 국가명

### 파일 경로
- `flag_image_path`: 국기 이미지 상대 경로
  - 형식: "difficulty/filename.svg"
  - 예시: "beginner/korea.svg"

### 퀴즈 콘텐츠
- `question_text`: 영어 질문 ("Which country does this flag belong to?")
- `option_a`, `option_b`, `option_c`, `option_d`: 4지선다 선택지
- `correct_answer`: 정답 (country_name과 동일)
- `correct_option`: 정답 선택지 위치 (A/B/C/D)

## 데이터 품질 보장
- 모든 선택지는 실제 국가명
- 정답 위치 랜덤 배치
- 난이도별 균등 분배 (각 85개)
- 중복 없는 고유한 조합

## Canva 호환성
- UTF-8 인코딩
- CSV 표준 형식
- 특수문자 처리 완료
- 파일 경로 정규화
