#!/usr/bin/env python3
"""
CSV 파일에 GitHub Pages 이미지 URL 컬럼을 추가하는 스크립트
"""
import csv
import shutil
from pathlib import Path

def add_github_urls_to_csv():
    """CSV에 GitHub Pages URL 컬럼 추가"""
    print("🔗 GitHub Pages URL 컬럼 추가 중...")
    print("==" * 35)

    # GitHub Pages 기본 URL (사용자가 나중에 실제 저장소 URL로 변경 필요)
    github_base_url = "https://USERNAME.github.io/REPOSITORY"

    csv_file = Path("flag_quiz_data.csv")
    updated_csv_file = Path("flag_quiz_data_with_urls.csv")

    if not csv_file.exists():
        print(f"❌ CSV 파일을 찾을 수 없습니다: {csv_file}")
        return False

    # CSV 파일 읽기
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames
        rows = list(reader)

    print(f"📊 읽어온 데이터: {len(rows)}개 행")

    # 새 헤더에 image_url 컬럼 추가
    new_headers = list(headers)
    if 'image_url' not in new_headers:
        # flag_image_path 다음에 image_url 추가
        flag_path_index = new_headers.index('flag_image_path')
        new_headers.insert(flag_path_index + 1, 'image_url')

    # 각 행에 GitHub URL 추가
    updated_rows = []
    for row in rows:
        new_row = {}
        for header in new_headers:
            if header == 'image_url':
                # GitHub Pages URL 생성
                flag_path = row['flag_image_path']
                github_url = f"{github_base_url}/canva_upload_ready/flag_images/svg/{flag_path}"
                new_row[header] = github_url
            else:
                new_row[header] = row.get(header, '')
        updated_rows.append(new_row)

    # 새 CSV 파일 저장
    with open(updated_csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=new_headers)
        writer.writeheader()
        writer.writerows(updated_rows)

    # 백업 후 원본 파일 교체
    backup_file = Path("flag_quiz_data_before_github_urls.csv")
    if backup_file.exists():
        backup_file.unlink()

    shutil.move(csv_file, backup_file)
    shutil.move(updated_csv_file, csv_file)

    print("✅ GitHub Pages URL 컬럼 추가 완료!")
    print(f"  - 백업: {backup_file}")
    print(f"  - 업데이트: {csv_file}")

    # 샘플 출력
    print("\n🔗 URL 샘플:")
    for i, row in enumerate(updated_rows[:3]):
        print(f"  {row['quiz_id']:3s}: {row['image_url']}")
    print("  ...")

    print(f"\n⚠️  중요: GitHub 저장소 생성 후 다음 URL을 실제 저장소 URL로 변경하세요:")
    print(f"  {github_base_url}")

    return True

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
    print("🔗 GitHub Pages URL 추가 스크립트")
    print("==" * 35)

    # 1. GitHub URL 컬럼 추가
    if add_github_urls_to_csv():
        print("✅ URL 컬럼 추가 성공")
    else:
        print("❌ URL 컬럼 추가 실패")
        return

    # 2. Canva 폴더 동기화
    update_canva_csv()

    print("\n🎉 모든 작업이 완료되었습니다!")
    print("\n📋 변경 사항:")
    print("  - CSV에 image_url 컬럼 추가")
    print("  - GitHub Pages URL 자동 생성")
    print("  - Canva 폴더 동기화 완료")

    print("\n🚀 다음 단계:")
    print("  1. GitHub 저장소 생성 및 파일 업로드")
    print("  2. GitHub Pages 활성화")
    print("  3. CSV의 URL을 실제 저장소 URL로 변경")
    print("  4. Canva Bulk Create에서 image_url 컬럼 연결 테스트")

if __name__ == "__main__":
    main()