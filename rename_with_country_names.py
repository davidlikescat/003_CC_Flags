#!/usr/bin/env python3
"""
SVG 파일명을 번호_국가명 형식으로 변경하는 스크립트
예: beginner01.svg → begin01_albania.svg
    intermediate01.svg → inter01_afghanistan.svg
    high01.svg → high01_andorra.svg
"""
import os
import shutil
import csv
import re
from pathlib import Path

def clean_country_name_for_filename(country_name):
    """국가명을 파일명에 적합하게 정리"""
    # 특수문자 제거 및 공백을 언더스코어로 변경
    cleaned = re.sub(r'[^\w\s-]', '', country_name)
    cleaned = re.sub(r'\s+', '_', cleaned.strip())
    cleaned = cleaned.lower()

    # 연속된 언더스코어 제거
    cleaned = re.sub(r'_+', '_', cleaned)
    cleaned = cleaned.strip('_')

    return cleaned

def get_csv_mapping():
    """CSV 파일에서 difficulty_number와 country_filename 매핑 가져오기"""
    csv_file = Path("flag_quiz_data.csv")

    if not csv_file.exists():
        print(f"❌ CSV 파일을 찾을 수 없습니다: {csv_file}")
        return {}

    mapping = {}

    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            difficulty_number = row['difficulty_number']
            country_filename = row['country_filename']
            mapping[difficulty_number] = country_filename

    return mapping

def rename_svg_files():
    """SVG 파일들을 새로운 형식으로 이름 변경"""
    print("🔄 SVG 파일명 변경 시작...")
    print("형식: begin01_albania.svg, inter01_afghanistan.svg, high01_andorra.svg")
    print("=" * 80)

    # CSV에서 매핑 정보 가져오기
    mapping = get_csv_mapping()
    if not mapping:
        print("❌ CSV 매핑 정보를 가져올 수 없습니다.")
        return False

    base_path = Path("canva_upload_ready/flag_images/svg")
    difficulties = ['beginner', 'intermediate', 'high']

    # 새 파일명 매핑 저장 (old_path → new_filename)
    filename_changes = {}

    for difficulty in difficulties:
        print(f"\n📁 {difficulty.upper()} 처리 중...")

        difficulty_path = base_path / difficulty
        if not difficulty_path.exists():
            print(f"❌ 폴더를 찾을 수 없습니다: {difficulty_path}")
            continue

        # 현재 폴더의 모든 SVG 파일 가져오기
        svg_files = list(difficulty_path.glob("*.svg"))

        # 임시 폴더 생성
        temp_path = difficulty_path.parent / f"{difficulty}_temp"
        if temp_path.exists():
            shutil.rmtree(temp_path)
        temp_path.mkdir()

        for svg_file in svg_files:
            # 현재 파일명에서 difficulty_number 추출
            current_filename = svg_file.stem  # 확장자 제거

            # 매핑에서 국가명 찾기
            if current_filename in mapping:
                country_filename = mapping[current_filename]

                # 새 파일명 생성
                # beginner01 → begin01, intermediate01 → inter01, high01 → high01
                if current_filename.startswith('beginner'):
                    prefix = 'begin'
                    number = current_filename.replace('beginner', '')
                elif current_filename.startswith('intermediate'):
                    prefix = 'inter'
                    number = current_filename.replace('intermediate', '')
                elif current_filename.startswith('high'):
                    prefix = 'high'
                    number = current_filename.replace('high', '')
                else:
                    print(f"⚠️  알 수 없는 형식: {current_filename}")
                    continue

                # 국가명 정리
                clean_country = clean_country_name_for_filename(country_filename)
                new_filename = f"{prefix}{number}_{clean_country}"
                new_filepath = temp_path / f"{new_filename}.svg"

                # 파일 복사
                shutil.copy2(svg_file, new_filepath)
                filename_changes[svg_file] = new_filename

                print(f"  ✅ {current_filename}.svg → {new_filename}.svg")
            else:
                print(f"  ⚠️  매핑을 찾을 수 없음: {current_filename}")

        # 기존 파일 삭제 후 새 파일들 이동
        for file in difficulty_path.glob("*.svg"):
            file.unlink()

        for file in temp_path.glob("*.svg"):
            shutil.move(file, difficulty_path)

        # 임시 폴더 삭제
        temp_path.rmdir()

    return filename_changes

def update_csv_with_new_filenames(filename_changes):
    """CSV 파일의 flag_image_path 업데이트"""
    print("\n📊 CSV 파일 업데이트 중...")
    print("=" * 60)

    csv_file = Path("flag_quiz_data.csv")
    updated_csv_file = Path("flag_quiz_data_updated.csv")

    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames
        rows = list(reader)

    updated_rows = []

    for row in rows:
        difficulty = row['difficulty']
        difficulty_number = row['difficulty_number']

        # filename_changes에서 새 파일명 찾기
        new_filename = None
        for old_path, new_name in filename_changes.items():
            if old_path.stem == difficulty_number:
                new_filename = new_name
                break

        if new_filename:
            # flag_image_path 업데이트
            row['flag_image_path'] = f"{difficulty}/{new_filename}.svg"
            print(f"✅ {row['quiz_id']:3s}: {difficulty_number} → {new_filename}")
        else:
            print(f"⚠️  파일명 변경 정보를 찾을 수 없음: {difficulty_number}")

        updated_rows.append(row)

    # 새 CSV 파일 저장
    with open(updated_csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(updated_rows)

    # 백업 후 교체
    backup_file = Path("flag_quiz_data_before_rename.csv")
    if backup_file.exists():
        backup_file.unlink()
    shutil.move(csv_file, backup_file)
    shutil.move(updated_csv_file, csv_file)

    print(f"\n💾 CSV 업데이트 완료!")
    print(f"  - 백업: {backup_file}")
    print(f"  - 업데이트: {csv_file}")

def update_canva_ready_csv():
    """canva_upload_ready 폴더의 CSV도 업데이트"""
    print("\n📦 Canva 업로드 폴더 CSV 동기화...")

    source_csv = Path("flag_quiz_data.csv")
    dest_csv = Path("canva_upload_ready/csv_data/flag_quiz_data.csv")

    if source_csv.exists() and dest_csv.parent.exists():
        shutil.copy2(source_csv, dest_csv)
        print("✅ Canva 업로드 폴더 CSV 동기화 완료")

def main():
    """메인 실행 함수"""
    print("🏷️ SVG 파일명 변경 스크립트")
    print("형식: begin01_albania.svg, inter01_afghanistan.svg, high01_andorra.svg")
    print("=" * 80)

    # 1. SVG 파일명 변경
    filename_changes = rename_svg_files()

    if not filename_changes:
        print("❌ 파일명 변경에 실패했습니다.")
        return

    # 2. CSV 파일 업데이트
    update_csv_with_new_filenames(filename_changes)

    # 3. Canva 업로드 폴더 동기화
    update_canva_ready_csv()

    print("\n🎉 모든 작업이 완료되었습니다!")
    print("\n📋 변경 사항:")
    print("  - SVG 파일명: 번호_국가명 형식으로 변경")
    print("  - CSV: flag_image_path 업데이트")
    print("  - Canva 폴더: 동기화 완료")

    print("\n📂 새 파일명 예시:")
    print("  begin01_albania.svg")
    print("  inter01_afghanistan.svg")
    print("  high01_andorra.svg")

if __name__ == "__main__":
    main()