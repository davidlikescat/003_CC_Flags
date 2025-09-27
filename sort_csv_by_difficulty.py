#!/usr/bin/env python3
"""
CSV 파일을 difficulty_number 컬럼 기준으로 순차 정렬하는 스크립트
beginner01, beginner02... intermediate01, intermediate02... high01, high02... 순서로 정렬
"""
import csv
import shutil
from pathlib import Path

def sort_csv_by_difficulty_number():
    """CSV 파일을 difficulty_number 기준으로 정렬"""
    print("📊 CSV 파일 정렬 시작...")
    print("정렬 기준: difficulty_number (beginner01~85, intermediate01~85, high01~85)")
    print("=" * 70)

    csv_file = Path("flag_quiz_data.csv")
    sorted_csv_file = Path("flag_quiz_data_sorted.csv")

    if not csv_file.exists():
        print(f"❌ CSV 파일을 찾을 수 없습니다: {csv_file}")
        return False

    # CSV 파일 읽기
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames
        rows = list(reader)

    print(f"📈 읽어온 데이터: {len(rows)}개 행")

    # 정렬 함수 정의
    def sort_key(row):
        """정렬 키 생성 함수"""
        difficulty_number = row['difficulty_number']

        # 난이도별 우선순위 설정
        if difficulty_number.startswith('beginner'):
            priority = 1
            number = int(difficulty_number.replace('beginner', ''))
        elif difficulty_number.startswith('intermediate'):
            priority = 2
            number = int(difficulty_number.replace('intermediate', ''))
        elif difficulty_number.startswith('high'):
            priority = 3
            number = int(difficulty_number.replace('high', ''))
        else:
            priority = 4
            number = 999

        return (priority, number)

    # 정렬 실행
    print("🔄 정렬 중...")
    sorted_rows = sorted(rows, key=sort_key)

    # quiz_id 재할당 (1번부터 순차적으로)
    print("🔢 quiz_id 재할당 중...")
    for i, row in enumerate(sorted_rows, 1):
        row['quiz_id'] = str(i)

    # 새 CSV 파일로 저장
    with open(sorted_csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(sorted_rows)

    # 백업 후 원본 파일 교체
    backup_file = Path("flag_quiz_data_before_sort.csv")
    if backup_file.exists():
        backup_file.unlink()

    shutil.move(csv_file, backup_file)
    shutil.move(sorted_csv_file, csv_file)

    print("💾 파일 저장 완료!")
    print(f"  - 정렬된 파일: {csv_file}")
    print(f"  - 백업 파일: {backup_file}")

    return True

def verify_sorting():
    """정렬 결과 검증"""
    print("\n🔍 정렬 결과 검증 중...")
    print("-" * 50)

    csv_file = Path("flag_quiz_data.csv")

    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        current_difficulty = ""
        current_number = 0
        count = 0

        for row in reader:
            count += 1
            difficulty_number = row['difficulty_number']

            # 첫 10개와 마지막 10개, 그리고 난이도 변경점 출력
            if count <= 10 or count > 245 or difficulty_number.startswith('intermediate01') or difficulty_number.startswith('high01'):
                print(f"  {row['quiz_id']:3s}: {difficulty_number} - {row['country_name']}")
            elif count == 11:
                print("  ...")

    print(f"\n✅ 총 {count}개 행 정렬 완료")

def update_canva_csv():
    """canva_upload_ready 폴더의 CSV도 업데이트"""
    print("\n📦 Canva 업로드 폴더 동기화...")

    source_csv = Path("flag_quiz_data.csv")
    dest_csv = Path("canva_upload_ready/csv_data/flag_quiz_data.csv")

    if source_csv.exists() and dest_csv.parent.exists():
        shutil.copy2(source_csv, dest_csv)
        print("✅ Canva 업로드 폴더 CSV 동기화 완료")

def main():
    """메인 실행 함수"""
    print("📊 CSV 파일 difficulty_number 순차 정렬")
    print("=" * 70)

    # 1. CSV 정렬
    if sort_csv_by_difficulty_number():
        print("✅ 정렬 성공")
    else:
        print("❌ 정렬 실패")
        return

    # 2. 정렬 결과 검증
    verify_sorting()

    # 3. Canva 폴더 동기화
    update_canva_csv()

    print("\n🎉 모든 작업이 완료되었습니다!")
    print("\n📋 변경 사항:")
    print("  - CSV 파일이 difficulty_number 순서로 정렬됨")
    print("  - quiz_id가 1~255로 재할당됨")
    print("  - 순서: beginner01~85 → intermediate01~85 → high01~85")

if __name__ == "__main__":
    main()