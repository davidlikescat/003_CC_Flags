#!/usr/bin/env python3
"""
Canva 업로드용 파일 구조 최적화 스크립트
- 업로드 준비 완료된 폴더 구조 생성
- 메타데이터 및 사용 가이드 생성
- 백업 및 버전 관리
"""
import os
import shutil
import json
from pathlib import Path
from datetime import datetime

def create_canva_ready_structure():
    """Canva 업로드용 최적화된 폴더 구조 생성"""
    print("📁 Canva 업로드용 파일 구조 최적화...")
    print("=" * 60)

    # 최종 출력 폴더 생성
    output_base = Path("canva_upload_ready")
    if output_base.exists():
        shutil.rmtree(output_base)
    output_base.mkdir()

    # 하위 폴더 구조 생성
    folders = {
        'csv_data': 'CSV 퀴즈 데이터',
        'flag_images': '국기 이미지 파일',
        'documentation': '사용 가이드 및 문서',
        'backup': '원본 백업',
        'metadata': '메타데이터'
    }

    for folder, description in folders.items():
        (output_base / folder).mkdir()
        print(f"✅ 폴더 생성: {folder}/ ({description})")

    return output_base

def copy_csv_data(output_base):
    """CSV 데이터 파일 복사"""
    print("\n📊 CSV 데이터 파일 복사 중...")

    csv_source = Path("flag_quiz_data.csv")
    csv_dest = output_base / "csv_data" / "flag_quiz_data.csv"

    if csv_source.exists():
        shutil.copy2(csv_source, csv_dest)
        print(f"✅ CSV 파일 복사: {csv_dest}")
    else:
        print(f"❌ CSV 파일을 찾을 수 없습니다: {csv_source}")

def copy_flag_images(output_base):
    """국기 이미지 파일 복사 (SVG 우선, PNG 대안)"""
    print("\n🎨 국기 이미지 파일 복사 중...")

    svg_source = Path("country-flags/svg_renamed")
    images_dest = output_base / "flag_images"

    if svg_source.exists():
        shutil.copytree(svg_source, images_dest / "svg", dirs_exist_ok=True)
        print(f"✅ SVG 파일 복사: {images_dest}/svg/")

        # 각 난이도별 파일 수 확인
        for difficulty in ['beginner', 'intermediate', 'high']:
            diff_path = images_dest / "svg" / difficulty
            if diff_path.exists():
                file_count = len(list(diff_path.glob("*.svg")))
                print(f"  - {difficulty}: {file_count}개 SVG 파일")
    else:
        print(f"❌ SVG 폴더를 찾을 수 없습니다: {svg_source}")

    # PNG 파일이 있다면 복사
    png_source = Path("country-flags/png_renamed")
    if png_source.exists():
        shutil.copytree(png_source, images_dest / "png", dirs_exist_ok=True)
        print(f"✅ PNG 파일 복사: {images_dest}/png/")

def create_usage_guide(output_base):
    """Canva 사용 가이드 생성"""
    print("\n📋 사용 가이드 생성 중...")

    guide_content = """# Canva 국기 퀴즈 영상 제작 가이드

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
- 국기 이미지 → `flag_image_path` 컬럼
- 질문 텍스트 → `question_text` 컬럼
- 선택지 A → `option_a` 컬럼
- 선택지 B → `option_b` 컬럼
- 선택지 C → `option_c` 컬럼
- 선택지 D → `option_d` 컬럼

### 4단계: 생성 및 다운로드
1. "Generate designs" 클릭 → 255개 영상 자동 생성
2. "Download all" → MP4 형식으로 일괄 다운로드

## 📊 CSV 데이터 구조

| 컬럼명 | 설명 | 예시 |
|--------|------|------|
| quiz_id | 퀴즈 번호 | 1, 2, 3... |
| difficulty | 난이도 | beginner, intermediate, high |
| country_name | 정답 국가명 | Korea, United States |
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
"""

    guide_path = output_base / "documentation" / "canva_usage_guide.md"
    with open(guide_path, 'w', encoding='utf-8') as f:
        f.write(guide_content)

    print(f"✅ 사용 가이드 생성: {guide_path}")

def create_csv_structure_doc(output_base):
    """CSV 구조 설명 문서 생성"""
    csv_doc_content = """# CSV 데이터 구조 상세 설명

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
"""

    csv_doc_path = output_base / "documentation" / "csv_structure.md"
    with open(csv_doc_path, 'w', encoding='utf-8') as f:
        f.write(csv_doc_content)

    print(f"✅ CSV 구조 문서 생성: {csv_doc_path}")

def create_metadata(output_base):
    """메타데이터 파일 생성"""
    print("\n🏷️ 메타데이터 생성 중...")

    metadata = {
        "project_name": "Flag Quiz Video Generator",
        "created_date": datetime.now().isoformat(),
        "total_quizzes": 255,
        "difficulty_distribution": {
            "beginner": 85,
            "intermediate": 85,
            "high": 85
        },
        "file_formats": ["SVG", "CSV"],
        "target_platform": "Canva Bulk Create",
        "video_duration": "15 seconds",
        "language": "English",
        "csv_structure": {
            "columns": 12,
            "encoding": "UTF-8",
            "format": "CSV"
        },
        "image_details": {
            "total_images": 255,
            "format": "SVG",
            "organized_by": "difficulty",
            "naming_convention": "country_name_lowercase_with_underscores"
        }
    }

    metadata_path = output_base / "metadata" / "project_metadata.json"
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)

    print(f"✅ 메타데이터 생성: {metadata_path}")

def create_backup(output_base):
    """중요 파일들 백업"""
    print("\n💾 백업 생성 중...")

    backup_items = [
        ("country-flags/countries.json", "countries_original.json"),
        ("flag_quiz_data.csv", "flag_quiz_data_backup.csv")
    ]

    backup_dir = output_base / "backup"

    for source, dest_name in backup_items:
        source_path = Path(source)
        if source_path.exists():
            dest_path = backup_dir / dest_name
            shutil.copy2(source_path, dest_path)
            print(f"✅ 백업 완료: {dest_name}")

def main():
    """메인 실행 함수"""
    print("🚀 Canva 업로드 준비 최적화 시작")
    print("=" * 60)

    # 1. 폴더 구조 생성
    output_base = create_canva_ready_structure()

    # 2. CSV 데이터 복사
    copy_csv_data(output_base)

    # 3. 국기 이미지 복사
    copy_flag_images(output_base)

    # 4. 사용 가이드 생성
    create_usage_guide(output_base)
    create_csv_structure_doc(output_base)

    # 5. 메타데이터 생성
    create_metadata(output_base)

    # 6. 백업 생성
    create_backup(output_base)

    # 결과 요약
    print("\n" + "=" * 60)
    print("🎉 Canva 업로드 준비 완료!")
    print(f"📁 출력 폴더: {output_base}")
    print("\n📋 다음 단계:")
    print("1. canva_upload_ready/ 폴더 확인")
    print("2. documentation/canva_usage_guide.md 읽기")
    print("3. Canva Pro에서 Bulk Create 사용")
    print("4. csv_data/flag_quiz_data.csv 업로드")
    print("5. 255개 퀴즈 영상 자동 생성!")

if __name__ == "__main__":
    main()