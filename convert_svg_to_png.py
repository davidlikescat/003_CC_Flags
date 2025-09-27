#!/usr/bin/env python3
"""
SVG 국기 파일을 PNG로 일괄 변환하는 스크립트
Canva 호환성을 위한 이미지 전처리
"""
import os
import subprocess
from pathlib import Path

def check_dependencies():
    """필요한 의존성 검사"""
    try:
        # ImageMagick convert 명령어 확인
        result = subprocess.run(['convert', '-version'],
                              capture_output=True, text=True, check=True)
        print("✅ ImageMagick이 설치되어 있습니다.")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ ImageMagick이 설치되어 있지 않습니다.")
        print("설치 방법:")
        print("  macOS: brew install imagemagick")
        print("  Ubuntu: sudo apt-get install imagemagick")
        print("  Windows: https://imagemagick.org/script/download.php")
        return False

def convert_svg_to_png(svg_path, png_path, size=512):
    """SVG를 PNG로 변환"""
    try:
        # ImageMagick 먼저 시도
        try:
            cmd = [
                'convert',
                '-background', 'transparent',
                '-size', f'{size}x{size}',
                str(svg_path),
                str(png_path)
            ]
            subprocess.run(cmd, check=True, capture_output=True)
            return True
        except subprocess.CalledProcessError:
            # ImageMagick 실패시 cairosvg 사용
            import cairosvg
            with open(svg_path, 'rb') as svg_file:
                cairosvg.svg2png(
                    file_obj=svg_file,
                    write_to=str(png_path),
                    output_width=size,
                    output_height=size
                )
            return True
    except Exception as e:
        print(f"❌ 변환 실패: {svg_path} -> {e}")
        return False

def convert_flags_to_png():
    """모든 국기 SVG 파일을 PNG로 변환"""
    print("🎨 SVG → PNG 변환 시작...")
    print("=" * 60)

    # 의존성 확인
    if not check_dependencies():
        return False

    base_path = Path("canva_upload_ready/flag_images/svg")

    if not base_path.exists():
        print(f"❌ 폴더를 찾을 수 없습니다: {base_path}")
        return False

    # PNG 출력 폴더 생성
    png_base_path = Path("canva_upload_ready/flag_images/png")
    if png_base_path.exists():
        import shutil
        shutil.rmtree(png_base_path)

    png_base_path.mkdir(parents=True, exist_ok=True)

    # 난이도별 폴더명
    difficulties = ['beginner', 'interm', 'high']

    success_count = 0
    total_count = 0

    print("\n🔄 변환 진행상황:")
    print("-" * 60)

    # 각 난이도별로 변환
    for difficulty in difficulties:
        svg_dir = base_path / difficulty

        if not svg_dir.exists():
            print(f"⚠️  폴더 없음: {svg_dir}")
            continue

        print(f"\n📁 {difficulty.upper()} 폴더 변환 중...")

        svg_files = list(svg_dir.glob("*.svg"))
        for svg_file in svg_files:
            total_count += 1
            # 파일명 그대로, 확장자만 png로 변경
            png_file = png_base_path / (svg_file.name.replace('.svg', '.png'))

            print(f"  🔄 {svg_file.name} -> {png_file.name}", end=" ")

            if convert_svg_to_png(svg_file, png_file):
                success_count += 1
                print("✅")
            else:
                print("❌")

    # 결과 요약
    print("\n" + "=" * 60)
    print(f"📊 변환 완료!")
    print(f"✅ 성공: {success_count}개")
    print(f"❌ 실패: {total_count - success_count}개")
    print(f"📁 PNG 파일 위치: {png_base_path}")

    # 파일 수 확인
    if png_base_path.exists():
        file_count = len(list(png_base_path.glob("*.png")))
        print(f"  - PNG 파일: {file_count}개")

    return success_count > 0

def create_alternative_method():
    """ImageMagick 없을 때 대안 방법 안내"""
    print("\n💡 ImageMagick 없이 변환하는 방법:")
    print("1. 온라인 변환 도구:")
    print("   - https://convertio.co/svg-png/")
    print("   - https://cloudconvert.com/svg-to-png")

    print("\n2. Python 라이브러리 사용:")
    print("   pip install cairosvg")
    print("   (별도 스크립트 필요)")

    print("\n3. Canva에서 직접 SVG 업로드:")
    print("   - Canva는 SVG 파일도 지원합니다")
    print("   - PNG 변환 없이 바로 사용 가능할 수 있습니다")

if __name__ == "__main__":
    print("🎨 국기 SVG → PNG 변환기")
    print("Canva 호환성을 위한 이미지 전처리")
    print("=" * 60)

    success = convert_flags_to_png()

    if not success:
        create_alternative_method()
    else:
        print("\n🎉 PNG 변환이 완료되었습니다!")
        print("이제 Canva에서 PNG 파일들을 사용할 수 있습니다.")