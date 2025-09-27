#!/usr/bin/env python3
"""
Canva 국기 퀴즈 영상용 CSV 데이터 생성 스크립트
- 255개 국기를 난이도별로 분류된 퀴즈 데이터로 변환
- 4지선다 오답 생성 로직 포함
- Canva Bulk Create 호환 형식
"""
import json
import csv
import os
import random
from pathlib import Path

def load_countries_data():
    """countries.json에서 국가 데이터 로드"""
    with open('country-flags/countries.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def get_country_pools():
    """난이도별 국가 풀 생성"""
    countries_data = load_countries_data()

    # 파일명 기준으로 실제 존재하는 국가들 확인
    beginner_files = set(f.replace('.svg', '') for f in os.listdir('country-flags/svg_renamed/beginner'))
    intermediate_files = set(f.replace('.svg', '') for f in os.listdir('country-flags/svg_renamed/intermediate'))
    high_files = set(f.replace('.svg', '') for f in os.listdir('country-flags/svg_renamed/high'))

    # 국가 코드를 국가명으로 매핑
    country_name_map = {}
    for code, name in countries_data.items():
        # 파일명 형식으로 변환 (소문자, 특수문자 처리)
        clean_name = name.lower()
        clean_name = clean_name.replace(' ', '_')
        clean_name = clean_name.replace(',', '')
        clean_name = clean_name.replace('(', '').replace(')', '')
        clean_name = clean_name.replace("'", "")
        clean_name = clean_name.replace('-', '_')
        clean_name = clean_name.replace('__', '_')

        # 특별한 경우들 처리
        special_cases = {
            'korea_republic_of': 'korea',
            'korea_democratic_people_s_republic_of': 'korea_democratic_peoples',
            'china_people_s_republic_of_china': 'china',
            'iran_islamic_republic_of': 'iran_islamic',
            'venezuela_bolivarian_republic_of': 'venezuela_bolivarian',
            'bolivia_plurinational_state_of': 'bolivia_plurinational',
            'congo_the_democratic_republic_of_the': 'congo_the_democratic_the',
            'côte_d_ivoire': 'côte_divoire',
            'micronesia_federated_states_of': 'micronesia',
            'laos_lao_people_s_democratic_republic': 'laos',
            'tanzania_united_republic_of': 'tanzania_united',
            'taiwan_republic_of_china': 'taiwan',
            'republic_of_türkiye': 'republic_of_türkiye'
        }

        if clean_name in special_cases:
            clean_name = special_cases[clean_name]

        country_name_map[clean_name] = name

    # 실제 파일과 매칭되는 국가들만 추출
    beginner_countries = [(f, country_name_map.get(f, f.replace('_', ' ').title())) for f in beginner_files]
    intermediate_countries = [(f, country_name_map.get(f, f.replace('_', ' ').title())) for f in intermediate_files]
    high_countries = [(f, country_name_map.get(f, f.replace('_', ' ').title())) for f in high_files]

    return {
        'beginner': beginner_countries,
        'intermediate': intermediate_countries,
        'high': high_countries
    }

def generate_wrong_answers(correct_country, difficulty, all_countries_pool):
    """그럴듯한 오답 3개 생성"""
    # 정답과 같은 난이도의 다른 국가들에서 선택
    same_difficulty_pool = [country for country in all_countries_pool[difficulty]
                           if country[1] != correct_country[1]]

    # 다른 난이도에서도 가져오기 (더 다양한 선택지)
    other_pools = []
    for diff in ['beginner', 'intermediate', 'high']:
        if diff != difficulty:
            other_pools.extend(all_countries_pool[diff])

    # 전체 풀에서 정답 제외
    total_pool = same_difficulty_pool + other_pools
    total_pool = [country for country in total_pool if country[1] != correct_country[1]]

    # 랜덤하게 3개 선택
    if len(total_pool) >= 3:
        wrong_answers = random.sample(total_pool, 3)
        return [country[1] for country in wrong_answers]
    else:
        # 풀이 부족한 경우 (실제로는 발생하지 않을 것)
        return ['오답1', '오답2', '오답3']

def create_quiz_csv():
    """퀴즈용 CSV 파일 생성"""
    print("🎯 국기 퀴즈 CSV 데이터 생성 시작...")
    print("=" * 60)

    # 국가 데이터 로드
    countries_pool = get_country_pools()

    # CSV 헤더
    csv_headers = [
        'quiz_id',
        'difficulty',
        'country_filename',
        'country_name',
        'flag_image_path',
        'question_text',
        'option_a',
        'option_b',
        'option_c',
        'option_d',
        'correct_answer',
        'correct_option'
    ]

    quiz_data = []
    quiz_id = 1

    print("\n📝 퀴즈 데이터 생성 중...")

    # 각 난이도별로 퀴즈 생성
    for difficulty in ['beginner', 'intermediate', 'high']:
        print(f"\n🎯 {difficulty.upper()} 난이도 처리 중...")

        countries = countries_pool[difficulty]
        for country_file, country_name in countries:
            # 오답 3개 생성
            wrong_answers = generate_wrong_answers((country_file, country_name), difficulty, countries_pool)

            # 선택지 섞기 (정답 위치 랜덤화)
            options = [country_name] + wrong_answers
            random.shuffle(options)

            # 정답이 몇 번째 선택지인지 찾기
            correct_option_index = options.index(country_name)
            correct_option_letter = ['A', 'B', 'C', 'D'][correct_option_index]

            quiz_item = {
                'quiz_id': quiz_id,
                'difficulty': difficulty,
                'country_filename': country_file,
                'country_name': country_name,
                'flag_image_path': f"{difficulty}/{country_file}.svg",
                'question_text': f"Which country does this flag belong to?",
                'option_a': options[0],
                'option_b': options[1],
                'option_c': options[2],
                'option_d': options[3],
                'correct_answer': country_name,
                'correct_option': correct_option_letter
            }

            quiz_data.append(quiz_item)
            print(f"✅ #{quiz_id:3d} {country_name} ({difficulty})")
            quiz_id += 1

    # CSV 파일로 저장
    csv_filename = 'flag_quiz_data.csv'
    print(f"\n💾 CSV 파일 저장 중: {csv_filename}")

    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_headers)
        writer.writeheader()
        writer.writerows(quiz_data)

    # 결과 요약
    print("\n" + "=" * 60)
    print(f"📊 퀴즈 데이터 생성 완료!")
    print(f"📁 파일명: {csv_filename}")
    print(f"📈 총 퀴즈 수: {len(quiz_data)}개")

    difficulty_counts = {}
    for item in quiz_data:
        diff = item['difficulty']
        difficulty_counts[diff] = difficulty_counts.get(diff, 0) + 1

    for difficulty, count in difficulty_counts.items():
        print(f"  - {difficulty.capitalize()}: {count}개")

    print(f"\n🎬 Canva Bulk Create 준비 완료!")
    print(f"   - CSV 파일을 Canva에 업로드하여 255개 퀴즈 영상을 자동 생성할 수 있습니다")

    return csv_filename

if __name__ == "__main__":
    print("🏴 Canva 국기 퀴즈 데이터 생성기")
    print("=" * 60)

    # 랜덤 시드 설정 (재현 가능한 결과)
    random.seed(42)

    try:
        csv_file = create_quiz_csv()
        print(f"\n🎉 완료! {csv_file} 파일이 생성되었습니다.")
    except Exception as e:
        print(f"\n❌ 오류 발생: {str(e)}")