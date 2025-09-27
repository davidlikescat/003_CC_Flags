#!/usr/bin/env python3
"""
국기를 난이도별로 분류하는 스크립트 (전세계 인지도 기준)
beginner, intermediate, high 폴더로 각각 85개씩 균등 분배
"""
import os
import shutil
from pathlib import Path

def create_difficulty_classification():
    """국기를 난이도별로 분류"""

    # 경로 설정
    base_path = Path("country-flags/svg_renamed")

    if not base_path.exists():
        print(f"Error: {base_path} 폴더를 찾을 수 없습니다.")
        return False

    # 난이도별 폴더 생성
    beginner_path = base_path / "beginner"
    intermediate_path = base_path / "intermediate"
    high_path = base_path / "high"

    for folder in [beginner_path, intermediate_path, high_path]:
        if folder.exists():
            shutil.rmtree(folder)
        folder.mkdir()

    # 난이도별 국가 분류 (전세계 인지도 기준)

    # BEGINNER (85개) - 매우 유명한 국가들
    beginner_countries = [
        # 주요 강대국 & G7
        'united_states', 'china', 'japan', 'germany', 'france', 'united_kingdom',
        'italy', 'canada', 'russia', 'india', 'brazil',

        # 유럽 주요국
        'spain', 'netherlands', 'belgium', 'switzerland', 'austria', 'sweden',
        'norway', 'denmark', 'finland', 'poland', 'portugal', 'greece', 'ireland',

        # 아시아 주요국
        'korea', 'australia', 'thailand', 'singapore', 'malaysia', 'indonesia',
        'philippines', 'vietnam', 'turkey', 'israel', 'saudi_arabia', 'iran_islamic',

        # 아메리카 주요국
        'mexico', 'argentina', 'chile', 'colombia', 'peru', 'venezuela_bolivarian',

        # 아프리카 주요국
        'south_africa', 'egypt', 'nigeria', 'kenya', 'morocco', 'ethiopia',

        # 독특한 디자인으로 유명
        'nepal', 'libya', 'cyprus', 'lebanon', 'jamaica', 'pakistan', 'bangladesh',
        'sri_lanka', 'ukraine', 'czech_republic', 'slovakia', 'hungary', 'romania',
        'bulgaria', 'croatia', 'serbia', 'bosnia_and_herzegovina', 'albania', 'estonia',
        'latvia', 'lithuania', 'iceland', 'luxembourg', 'slovenia', 'malta', 'monaco',
        'new_zealand', 'fiji', 'papua_new_guinea', 'cuba', 'jamaica', 'costa_rica',
        'panama', 'uruguay', 'paraguay', 'bolivia_plurinational', 'ecuador', 'honduras',
        'guatemala', 'algeria', 'tunisia', 'libya', 'ghana', 'cameroon', 'zimbabwe'
    ]

    # INTERMEDIATE (85개) - 중간 인지도 국가들
    intermediate_countries = [
        # 유럽 중소국
        'czech_republic', 'slovakia', 'hungary', 'romania', 'bulgaria', 'croatia',
        'serbia', 'bosnia_and_herzegovina', 'montenegro', 'north_macedonia', 'albania',
        'kosovo', 'moldova', 'belarus', 'estonia', 'latvia', 'lithuania', 'iceland',
        'luxembourg', 'slovenia', 'malta', 'cyprus', 'monaco', 'liechtenstein', 'san_marino',

        # 아시아 중소국
        'myanmar', 'cambodia', 'laos', 'brunei_darussalam', 'mongolia', 'kazakhstan',
        'uzbekistan', 'kyrgyzstan', 'tajikistan', 'turkmenistan', 'afghanistan', 'iraq',
        'jordan', 'kuwait', 'qatar', 'bahrain', 'oman', 'yemen', 'georgia', 'armenia',
        'azerbaijan', 'nepal', 'bhutan', 'sri_lanka', 'maldives',

        # 오세아니아
        'new_zealand', 'fiji', 'papua_new_guinea', 'samoa', 'tonga', 'vanuatu',

        # 아메리카 중소국
        'cuba', 'jamaica', 'haiti', 'dominican_republic', 'costa_rica', 'panama',
        'nicaragua', 'honduras', 'guatemala', 'el_salvador', 'belize', 'uruguay',
        'paraguay', 'bolivia_plurinational', 'ecuador', 'guyana', 'suriname',

        # 아프리카 중간 인지도
        'algeria', 'tunisia', 'libya', 'sudan', 'ethiopia', 'somalia', 'ghana',
        'ivory_coast', 'senegal', 'mali', 'niger', 'burkina_faso', 'cameroon',
        'central_african_republic', 'chad', 'democratic_republic_congo', 'republic_congo',
        'gabon', 'zambia', 'zimbabwe', 'botswana', 'namibia', 'angola', 'mozambique',
        'madagascar', 'mauritius', 'seychelles'
    ]

    # HIGH (나머지 모든 국가들) - 작은 섬나라, 영토, 인지도 낮은 국가들
    # 전체 파일 목록에서 beginner, intermediate 제외한 나머지

    print("🏴 국기 난이도별 분류 시작...")
    print("=" * 60)

    # 모든 SVG 파일 목록 가져오기
    all_files = [f for f in os.listdir(base_path) if f.endswith('.svg')]
    print(f"총 파일 수: {len(all_files)}개")

    # 파일명에서 확장자 제거하여 국가명 추출
    all_countries = [f.replace('.svg', '') for f in all_files]

    # 분류 카운터
    beginner_count = 0
    intermediate_count = 0
    high_count = 0

    # Beginner 분류
    print(f"\n🟢 BEGINNER 폴더 생성 중...")
    for country in all_countries:
        if country in beginner_countries and beginner_count < 85:
            src = base_path / f"{country}.svg"
            dst = beginner_path / f"{country}.svg"
            if src.exists():
                shutil.copy2(src, dst)
                beginner_count += 1
                print(f"✅ {country}.svg → beginner/")

    # Intermediate 분류
    print(f"\n🟡 INTERMEDIATE 폴더 생성 중...")
    for country in all_countries:
        if country in intermediate_countries and intermediate_count < 85:
            src = base_path / f"{country}.svg"
            dst = intermediate_path / f"{country}.svg"
            if src.exists() and not (beginner_path / f"{country}.svg").exists():
                shutil.copy2(src, dst)
                intermediate_count += 1
                print(f"✅ {country}.svg → intermediate/")

    # High 분류 (나머지)
    print(f"\n🔴 HIGH 폴더 생성 중...")
    classified_countries = set()

    # 이미 분류된 국가들 체크
    for country in all_countries:
        if (beginner_path / f"{country}.svg").exists() or (intermediate_path / f"{country}.svg").exists():
            classified_countries.add(country)

    # 나머지 국가들을 High에 분류
    for country in all_countries:
        if country not in classified_countries and high_count < 85:
            src = base_path / f"{country}.svg"
            dst = high_path / f"{country}.svg"
            if src.exists():
                shutil.copy2(src, dst)
                high_count += 1
                print(f"✅ {country}.svg → high/")

    # 부족한 경우 재분배
    remaining_countries = []
    for country in all_countries:
        src = base_path / f"{country}.svg"
        if (src.exists() and
            not (beginner_path / f"{country}.svg").exists() and
            not (intermediate_path / f"{country}.svg").exists() and
            not (high_path / f"{country}.svg").exists()):
            remaining_countries.append(country)

    # 남은 국가들 균등 분배
    for i, country in enumerate(remaining_countries):
        src = base_path / f"{country}.svg"
        if beginner_count < 85:
            dst = beginner_path / f"{country}.svg"
            target_folder = "beginner"
            beginner_count += 1
        elif intermediate_count < 85:
            dst = intermediate_path / f"{country}.svg"
            target_folder = "intermediate"
            intermediate_count += 1
        elif high_count < 85:
            dst = high_path / f"{country}.svg"
            target_folder = "high"
            high_count += 1
        else:
            break

        shutil.copy2(src, dst)
        print(f"✅ {country}.svg → {target_folder}/ (재분배)")

    # 결과 요약
    print("\n" + "=" * 60)
    print(f"📊 분류 결과:")
    print(f"🟢 Beginner: {beginner_count}개")
    print(f"🟡 Intermediate: {intermediate_count}개")
    print(f"🔴 High: {high_count}개")
    print(f"📁 총 분류된 파일: {beginner_count + intermediate_count + high_count}개")

    print(f"\n📂 폴더 위치:")
    print(f"  - {beginner_path}")
    print(f"  - {intermediate_path}")
    print(f"  - {high_path}")

    return True

if __name__ == "__main__":
    print("🎯 국기 난이도별 분류 스크립트")
    print("전세계 인지도 기준으로 beginner/intermediate/high 분류")
    print("=" * 60)

    if create_difficulty_classification():
        print("\n🎉 난이도별 분류가 완료되었습니다!")
    else:
        print("\n💥 분류 중 오류가 발생했습니다.")