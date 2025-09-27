#!/usr/bin/env python3
"""
CSV 파일의 GitHub URL을 실제 저장소 URL로 업데이트하는 스크립트
"""
import csv
import shutil
from pathlib import Path

def update_github_urls():
    """CSV의 GitHub URL을 실제 저장소 URL로 업데이트"""
    print("🔗 GitHub URL 업데이트 중...")
    print("저장소: https://github.com/davidlikescat/003_CC_Flags")
    print("GitHub Pages: https://davidlikescat.github.io/003_CC_Flags")
    print("==" * 40)

    # 실제 GitHub Pages URL
    github_pages_url = "https://davidlikescat.github.io/003_CC_Flags"

    csv_file = Path("flag_quiz_data.csv")
    updated_csv_file = Path("flag_quiz_data_updated_urls.csv")

    if not csv_file.exists():
        print(f"❌ CSV 파일을 찾을 수 없습니다: {csv_file}")
        return False

    # CSV 파일 읽기
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames
        rows = list(reader)

    print(f"📊 업데이트할 데이터: {len(rows)}개 행")

    # URL 업데이트
    updated_rows = []
    for row in rows:
        if 'image_url' in row:
            # 기존 플레이스홀더 URL을 실제 GitHub Pages URL로 교체
            flag_path = row['flag_image_path']
            row['image_url'] = f"{github_pages_url}/canva_upload_ready/flag_images/svg/{flag_path}"
        updated_rows.append(row)

    # 새 CSV 파일 저장
    with open(updated_csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(updated_rows)

    # 백업 후 원본 파일 교체
    backup_file = Path("flag_quiz_data_placeholder_urls.csv")
    if backup_file.exists():
        backup_file.unlink()

    shutil.move(csv_file, backup_file)
    shutil.move(updated_csv_file, csv_file)

    print("✅ GitHub URL 업데이트 완료!")
    print(f"  - 백업: {backup_file}")
    print(f"  - 업데이트: {csv_file}")

    # 샘플 출력
    print("\n🔗 업데이트된 URL 샘플:")
    for i, row in enumerate(updated_rows[:3]):
        print(f"  {row['quiz_id']:3s}: {row['image_url']}")
    print("  ...")

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
    print("🔗 GitHub Pages URL 업데이트 스크립트")
    print("==" * 40)

    # 1. GitHub URL 업데이트
    if update_github_urls():
        print("✅ URL 업데이트 성공")
    else:
        print("❌ URL 업데이트 실패")
        return

    # 2. Canva 폴더 동기화
    update_canva_csv()

    print("\n🎉 모든 작업이 완료되었습니다!")
    print("\n📋 변경 사항:")
    print("  - CSV의 image_url을 실제 GitHub Pages URL로 업데이트")
    print("  - Canva 폴더 동기화 완료")

    print("\n🚀 다음 단계:")
    print("  1. 파일들을 GitHub 저장소에 업로드")
    print("  2. GitHub Pages 활성화")
    print("  3. Canva Bulk Create에서 image_url 컬럼 테스트")

if __name__ == "__main__":
    main()