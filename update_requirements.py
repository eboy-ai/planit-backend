import subprocess

# 현재 패키지 목록 가져오기
installed = subprocess.check_output(["pip", "freeze"]).decode().splitlines()

# 기존 requirements.txt 읽기
try:
    with open("requirements.txt", "r") as f:
        existing = set(f.read().splitlines())
except FileNotFoundError:
    existing = set()

# 새로 추가된 패키지 필터링
new_packages = [pkg for pkg in installed if pkg not in existing]

if new_packages:
    with open("requirements.txt", "a") as f:
        f.write("\n".join(new_packages) + "\n")
    print(f"{len(new_packages)}개 패키지 추가됨:")
    for p in new_packages:
        print(" +", p)
else:
    print("새 패키지 없음.")