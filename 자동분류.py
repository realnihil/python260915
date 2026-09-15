from pathlib import Path  # 운영체제에 맞는 파일 경로를 다루는 클래스
import shutil  # 파일 이동과 복사 기능을 제공하는 모듈


# 정리할 다운로드 폴더의 위치입니다.
# r을 앞에 붙이면 Windows 경로의 백슬래시를 그대로 사용할 수 있습니다.
DOWNLOAD_FOLDER = Path(r"C:\Users\student\Downloads")

# 폴더 이름을 키로, 해당 폴더로 보낼 확장자 집합을 값으로 저장합니다.
# 집합(set)은 여러 값을 중복 없이 저장할 때 사용합니다.
FILE_CATEGORIES = {
    "images": {".jpg", ".jpeg"},
    "data": {".csv", ".xlsx"},
    "docs": {".txt", ".doc", ".pdf"},
    "archive": {".zip", ".exe"},
}


def get_available_path(destination: Path) -> Path:
    """같은 이름의 파일이 있으면 덮어쓰지 않는 이동 대상 경로를 만듭니다."""
    # 대상 경로에 파일이 없으면 원래 경로를 그대로 사용합니다.
    if not destination.exists():
        return destination

    # 같은 이름의 파일이 있으면 파일명 뒤에 _1, _2와 같은 번호를 붙입니다.
    counter = 1
    while True:
        # stem은 확장자를 제외한 파일명이고 suffix는 확장자입니다.
        candidate = destination.with_name(
            f"{destination.stem}_{counter}{destination.suffix}"
        )
        # 번호가 붙은 후보 경로도 사용 중이면 다음 번호를 확인합니다.
        if not candidate.exists():
            return candidate
        counter += 1


def organize_downloads() -> None:
    """다운로드 폴더의 파일을 확장자별 폴더로 이동합니다."""
    # 다운로드 폴더가 실제로 존재하는지 먼저 확인합니다.
    if not DOWNLOAD_FOLDER.is_dir():
        print(f"다운로드 폴더를 찾을 수 없습니다: {DOWNLOAD_FOLDER}")
        return

    # 확장자로 목적지 폴더를 바로 찾을 수 있도록 하나의 사전으로 변환합니다.
    # 예: {".jpg": "images", ".pdf": "docs"}
    extension_to_folder = {
        extension: folder_name
        for folder_name, extensions in FILE_CATEGORIES.items()
        for extension in extensions
    }

    # 다운로드 폴더 안의 항목을 하나씩 확인합니다.
    for file_path in DOWNLOAD_FOLDER.iterdir():
        # 폴더는 건너뛰고 파일만 처리합니다.
        if not file_path.is_file():
            continue

        # 확장자를 소문자로 바꾸어 .JPG와 .jpg를 동일하게 처리합니다.
        folder_name = extension_to_folder.get(file_path.suffix.lower())
        # 분류 대상이 아닌 확장자는 건너뜁니다.
        if folder_name is None:
            continue

        # 목적지 폴더가 없으면 만듭니다.
        destination_folder = DOWNLOAD_FOLDER / folder_name
        destination_folder.mkdir(exist_ok=True)

        # 같은 이름의 파일이 있으면 번호가 붙은 새 경로를 사용합니다.
        destination = get_available_path(destination_folder / file_path.name)

        # 실제로 파일을 목적지 폴더로 이동합니다.
        shutil.move(str(file_path), str(destination))
        print(f"이동 완료: {file_path.name} -> {destination_folder}")


# 이 파일을 직접 실행했을 때만 정리 함수를 호출합니다.
# 다른 파일에서 import할 때는 자동으로 파일을 이동하지 않습니다.
if __name__ == "__main__":
    organize_downloads()
