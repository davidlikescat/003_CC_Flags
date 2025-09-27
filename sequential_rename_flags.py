#!/usr/bin/env python3
"""
국기 파일을 난이도별로 ABC 순서로 정렬하여 순차 넘버링하는 스크립트
beginner01, beginner02... intermediate01, intermediate02... high01, high02...
"""
import os
import shutil
import csv
from pathlib import Path

def rename_files_sequentially():
    """각 난이도별로 파일을 ABC 순서로 정렬하여 순차 넘버링"""
    print("🔢 국기 파일 순차 넘버링 시작...")
    print("=" * 60)

    base_path = Path("canva_upload_ready/flag_images/svg")
    difficulties = ['beginner', 'intermediate', 'high']

    # 파일명 매핑을 저장할 딕셔너리 (기존파일명 → 새파일명)
    filename_mapping = {}

    for difficulty in difficulties:
        print(f"\n📁 {difficulty.upper()} 처리 중...")

        difficulty_path = base_path / difficulty
        if not difficulty_path.exists():
            print(f"❌ 폴더를 찾을 수 없습니다: {difficulty_path}")
            continue

        # 현재 폴더의 모든 SVG 파일 가져오기
        svg_files = list(difficulty_path.glob("*.svg"))

        # ABC 순서로 정렬 (파일명 기준)
        svg_files.sort(key=lambda x: x.name.lower())

        print(f"  총 파일 수: {len(svg_files)}개")

        # 임시 폴더 생성 (충돌 방지)
        temp_path = difficulty_path.parent / f"{difficulty}_temp"
        if temp_path.exists():
            shutil.rmtree(temp_path)
        temp_path.mkdir()

        # 순차적으로 번호 부여하여 임시 폴더에 복사
        for i, svg_file in enumerate(svg_files, 1):
            # 기존 파일명에서 확장자 제거
            old_filename = svg_file.stem

            # 새 파일명 생성 (난이도 + 두자리 숫자)
            new_filename = f"{difficulty}{i:02d}"
            new_filepath = temp_path / f"{new_filename}.svg"

            # 파일 복사
            shutil.copy2(svg_file, new_filepath)

            # 매핑 정보 저장
            filename_mapping[old_filename] = new_filename

            print(f"  ✅ {old_filename}.svg → {new_filename}.svg")

        # 기존 폴더 내용 삭제 후 임시 폴더 내용 이동
        for file in difficulty_path.glob("*.svg"):
            file.unlink()

        for file in temp_path.glob("*.svg"):
            shutil.move(file, difficulty_path)

        # 임시 폴더 삭제
        temp_path.rmdir()

    print("\n" + "=" * 60)
    print(f"📊 파일명 변경 완료!")

    for difficulty in difficulties:
        difficulty_path = base_path / difficulty
        if difficulty_path.exists():
            file_count = len(list(difficulty_path.glob("*.svg")))
            print(f"  - {difficulty}: {file_count}개")

    return filename_mapping

def update_csv_with_numbering(filename_mapping):
    """CSV 파일에 새로운 넘버링 정보 추가"""
    print("\n📊 CSV 파일 업데이트 중...")
    print("=" * 60)

    csv_file = Path("flag_quiz_data.csv")
    updated_csv_file = Path("flag_quiz_data_numbered.csv")

    if not csv_file.exists():
        print(f"❌ CSV 파일을 찾을 수 없습니다: {csv_file}")
        return False

    # CSV 파일 읽기
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        headers = reader.fieldnames

    # 새로운 컬럼 추가
    new_headers = headers[:2] + ['difficulty_number'] + headers[2:]  # difficulty 다음에 추가

    updated_rows = []

    for row in rows:
        # 기존 파일명에서 새 넘버링 찾기
        old_filename = row['country_filename']
        difficulty = row['difficulty']

        # 매핑에서 새 파일명 찾기
        if old_filename in filename_mapping:
            new_number = filename_mapping[old_filename]
        else:
            # 매핑을 찾을 수 없는 경우 기본값 생성
            # 해당 난이도의 다른 파일들을 확인하여 순서 추정
            same_difficulty_files = [k for k, v in filename_mapping.items()
                                   if v.startswith(difficulty)]
            new_number = f"{difficulty}{len(same_difficulty_files)+1:02d}"

        # 새 행 생성
        new_row = {}
        for header in new_headers:
            if header == 'difficulty_number':
                new_row[header] = new_number
            elif header == 'flag_image_path':
                # 이미지 경로도 새 파일명으로 업데이트
                new_row[header] = f"{difficulty}/{new_number}.svg"
            else:
                new_row[header] = row[header]

        updated_rows.append(new_row)

        print(f"✅ {row['quiz_id']:3s}: {old_filename} → {new_number}")

    # 새 CSV 파일 저장
    with open(updated_csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=new_headers)
        writer.writeheader()
        writer.writerows(updated_rows)

    # 기존 파일을 백업하고 새 파일로 교체
    backup_file = Path("flag_quiz_data_backup.csv")
    if backup_file.exists():
        backup_file.unlink()
    shutil.move(csv_file, backup_file)
    shutil.move(updated_csv_file, csv_file)

    print(f"\n💾 CSV 파일 업데이트 완료!")
    print(f"  - 원본 백업: {backup_file}")
    print(f"  - 업데이트된 파일: {csv_file}")
    print(f"  - 새 컬럼 추가: difficulty_number")

    return True

def update_canva_ready_structure():
    """canva_upload_ready 폴더도 동일하게 업데이트"""
    print("\n📦 Canva 업로드 폴더 동기화 중...")

    # CSV 파일 복사
    source_csv = Path("flag_quiz_data.csv")
    dest_csv = Path("canva_upload_ready/csv_data/flag_quiz_data.csv")

    if source_csv.exists() and dest_csv.parent.exists():
        shutil.copy2(source_csv, dest_csv)
        print("✅ CSV 파일 동기화 완료")

    print("📦 Canva 업로드 준비 완료!")

def main():
    """메인 실행 함수"""
    print("🔢 국기 파일 순차 넘버링 스크립트")
    print("ABC 순서로 정렬하여 beginner01, intermediate01, high01... 형식으로 변경")
    print("=" * 80)

    # 현재 디렉토리 확인
    current_dir = Path.cwd()
    print(f"현재 디렉토리: {current_dir}")

    # 1. 파일명 순차 넘버링
    filename_mapping = rename_files_sequentially()

    if not filename_mapping:
        print("❌ 파일명 변경에 실패했습니다.")
        return

    # 2. CSV 파일 업데이트
    if update_csv_with_numbering(filename_mapping):
        print("✅ CSV 업데이트 성공")
    else:
        print("❌ CSV 업데이트 실패")

    # 3. Canva 업로드 폴더 동기화
    update_canva_ready_structure()

    print("\n🎉 모든 작업이 완료되었습니다!")
    print("\n📋 변경 사항:")
    print("  - 파일명: ABC 순서로 정렬하여 순차 넘버링")
    print("  - CSV: difficulty_number 컬럼 추가")
    print("  - 경로: flag_image_path 업데이트")

    print("\n📂 새 파일 구조 예시:")
    print("  beginner/beginner01.svg (albania.svg)")
    print("  beginner/beginner02.svg (algeria.svg)")
    print("  intermediate/intermediate01.svg (afghanistan.svg)")
    print("  high/high01.svg (åland_islands.svg)")

if __name__ == "__main__":
    main()