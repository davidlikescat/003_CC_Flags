#!/usr/bin/env python3
"""
국기 파일명을 국가 코드에서 영어 국가명으로 변경하는 스크립트
"""
import json
import os
import shutil
from pathlib import Path
import re

def clean_filename(name):
    """파일명을 영어로 정리하고 파일시스템에 안전하게 만들기"""
    # 특수문자와 괄호 내용 제거
    name = re.sub(r'\([^)]*\)', '', name)  # 괄호와 내용 제거
    name = re.sub(r'[^\w\s-]', '', name)  # 특수문자 제거 (영문, 숫자, 공백, 하이픈만 유지)
    name = re.sub(r'\s+', '_', name.strip())  # 공백을 언더스코어로 변경
    name = name.lower()  # 소문자로 변경

    # 특정 단어들 정리
    name = name.replace('_republic_of', '')
    name = name.replace('_state_of', '')
    name = name.replace('_kingdom_of', '')
    name = name.replace('_federation_of', '')
    name = name.replace('_democratic_republic_of_the', '')
    name = name.replace('_plurinational_state_of', '')
    name = name.replace('_islamic_republic_of', '')
    name = name.replace('_bolivarian_republic_of', '')
    name = name.replace('_federated_states_of', '')
    name = name.replace('_united_republic_of', '')

    # 연속된 언더스코어 제거
    name = re.sub(r'_+', '_', name)
    name = name.strip('_')

    return name

def rename_flag_files():
    """국기 파일들의 이름을 변경"""

    # 기본 경로 설정
    base_path = Path("country-flags")
    svg_path = base_path / "svg"
    countries_json_path = base_path / "countries.json"

    # countries.json 파일 읽기
    try:
        with open(countries_json_path, 'r', encoding='utf-8') as f:
            countries = json.load(f)
    except FileNotFoundError:
        print(f"Error: {countries_json_path} 파일을 찾을 수 없습니다.")
        return False
    except json.JSONDecodeError:
        print(f"Error: {countries_json_path} 파일의 JSON 형식이 올바르지 않습니다.")
        return False

    # SVG 폴더 확인
    if not svg_path.exists():
        print(f"Error: {svg_path} 폴더를 찾을 수 없습니다.")
        return False

    # 백업 폴더 생성
    backup_path = base_path / "svg_backup"
    if not backup_path.exists():
        print("원본 파일 백업 중...")
        shutil.copytree(svg_path, backup_path)
        print(f"백업 완료: {backup_path}")

    # 변경된 파일들을 저장할 새 폴더 생성
    renamed_path = base_path / "svg_renamed"
    if renamed_path.exists():
        shutil.rmtree(renamed_path)
    renamed_path.mkdir()

    success_count = 0
    failed_count = 0
    failed_files = []

    print("\n파일명 변경 시작...")
    print("-" * 60)

    # 각 국가 코드에 대해 파일명 변경
    for country_code, country_name in countries.items():
        old_filename = f"{country_code.lower()}.svg"
        old_filepath = svg_path / old_filename

        # 원본 파일이 존재하는지 확인
        if not old_filepath.exists():
            print(f"⚠️  파일 없음: {old_filename}")
            failed_count += 1
            failed_files.append(f"{old_filename} (파일 없음)")
            continue

        # 새 파일명 생성 (영어로 정리)
        clean_country_name = clean_filename(country_name)
        new_filename = f"{clean_country_name}.svg"
        new_filepath = renamed_path / new_filename

        try:
            # 파일 복사
            shutil.copy2(old_filepath, new_filepath)
            print(f"✅ {old_filename:<8} → {new_filename}")
            success_count += 1

        except Exception as e:
            print(f"❌ 실패: {old_filename} → {new_filename}")
            print(f"   오류: {str(e)}")
            failed_count += 1
            failed_files.append(f"{old_filename} ({str(e)})")

    # 결과 요약
    print("-" * 60)
    print(f"\n📊 변경 결과:")
    print(f"✅ 성공: {success_count}개")
    print(f"❌ 실패: {failed_count}개")

    if failed_files:
        print(f"\n실패한 파일들:")
        for failed_file in failed_files:
            print(f"  - {failed_file}")

    print(f"\n📁 변경된 파일 위치: {renamed_path}")
    print(f"📁 원본 백업 위치: {backup_path}")

    return success_count > 0

if __name__ == "__main__":
    print("🏴 국기 파일명 변경 스크립트 (영어 버전)")
    print("=" * 60)

    if rename_flag_files():
        print("\n🎉 파일명 변경이 완료되었습니다!")
        print("예시: kr.svg → korea.svg, us.svg → united_states.svg")
    else:
        print("\n💥 파일명 변경 중 오류가 발생했습니다.")