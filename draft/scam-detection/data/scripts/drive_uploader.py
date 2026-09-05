"""
================================================================================
DỰ ÁN CUỐI KỲ CS114 - MÁY HỌC (NHÓM 10 - UIT)
CÔNG CỤ TẢI MINH CHỨNG LÊN GOOGLE DRIVE (GOOGLE DRIVE EVIDENCE VAULT UPLOADER)
================================================================================
Mục đích:
  - Tự động hóa việc tải ảnh chụp màn hình tin nhắn SMS đời thực (bằng chứng) lên thư mục
    Google Drive chung của nhóm: `CS114_Evidence_Vault`.
  - Tự động thiết lập quyền xem (share link) và trả về đường link `https://drive.google.com/...`
    để dán trực tiếp vào cột `source_url` trên Google Sheet hoặc tệp `dataset.csv`.
  - Giúp kho Git không bị phình to dung lượng bởi file ảnh nhị phân lớn.
  - Sử dụng tệp xác thực OAuth 2.0 `credentials.json` (được bảo vệ, không commit lên Git).

Hướng dẫn sử dụng cho thành viên trong nhóm:
  1. Tải 1 ảnh chụp màn hình lên Drive:
     python3 drive_uploader.py --file "path/to/sms_screenshot.png"
  2. Tải hàng loạt ảnh từ 1 thư mục ảnh trên máy:
     python3 drive_uploader.py --folder "path/to/screenshots_folder"
  3. Lần đầu chạy, trình duyệt web sẽ tự động mở để bạn đăng nhập tài khoản Google và xác nhận.
     Sau đó thông tin đăng nhập sẽ lưu vào `token.json` cho các lần chạy tự động tiếp theo.
================================================================================
"""

from __future__ import annotations

import argparse
import mimetypes
import sys
from pathlib import Path
from typing import Final

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Thư mục Google Drive Evidence Vault mặc định của nhóm 10
DEFAULT_FOLDER_ID: Final[str] = "1YuXfFBHMWfpafBgykXKCzKDjqKAyE9DL"

# Quyền hạn truy cập: chỉ quản lý file do ứng dụng tạo ra trên Drive (an toàn nhất)
SCOPES: Final[list[str]] = ["https://www.googleapis.com/auth/drive.file"]


def get_project_root() -> Path:
    """Trả về thư mục draft/scam-detection."""
    current_path = Path(__file__).resolve()
    for parent in [current_path.parent, current_path.parent.parent, current_path.parent.parent.parent]:
        if (parent / "credentials.json").exists() or (parent / "src").exists():
            return parent
    return current_path.parent.parent


def authenticate_google_drive(credentials_path: Path, token_path: Path):
    """
    Xác thực tài khoản Google Drive qua OAuth 2.0 Client.
    Tự động tái sử dụng token.json hoặc mở trình duyệt cấp quyền trong lần đầu tiên.
    """
    creds = None
    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("[*] Đang làm mới phiên đăng nhập Google Drive...")
            creds.refresh(Request())
        else:
            if not credentials_path.exists():
                print(f"[!] Lỗi: Không tìm thấy tệp xác thực OAuth tại: {credentials_path}")
                print("[*] Vui lòng tải credentials.json từ Google Cloud Console và đặt vào thư mục draft/scam-detection/")
                sys.exit(1)

            print("[*] Đang mở trình duyệt để xác thực quyền Google Drive lần đầu...")
            flow = InstalledAppFlow.from_client_secrets_file(str(credentials_path), SCOPES)
            creds = flow.run_local_server(port=0)

        # Lưu token cho các lần sau
        with open(token_path, "w", encoding="utf-8") as token_file:
            token_file.write(creds.to_json())
        print(f"[+] Đã lưu phiên xác thực tại: {token_path.name}")

    return build("drive", "v3", credentials=creds)


def upload_single_file(service, file_path: Path, folder_id: str) -> str:
    """
    Tải một tệp ảnh/tài liệu lên Google Drive và trả về đường dẫn xem trực tiếp.
    """
    if not file_path.exists():
        print(f"[!] Không tìm thấy tệp: {file_path}")
        return ""

    mime_type, _ = mimetypes.guess_type(str(file_path))
    mime_type = mime_type or "application/octet-stream"

    file_metadata = {
        "name": file_path.name,
        "parents": [folder_id],
    }
    media = MediaFileUpload(str(file_path), mimetype=mime_type, resumable=True)

    print(f"[*] Đang tải lên: {file_path.name}...")
    uploaded_file = (
        service.files()
        .create(body=file_metadata, media_body=media, fields="id, name, webViewLink")
        .execute()
    )

    file_id = uploaded_file.get("id")
    web_link = uploaded_file.get("webViewLink")

    # Mở quyền xem cho bất kỳ ai có link (viewable with link)
    try:
        service.permissions().create(
            fileId=file_id,
            body={"type": "anyone", "role": "reader"},
        ).execute()
    except Exception as e:
        print(f"[*] Ghi chú quyền: {e}")

    print(f"[+] Thành công: {file_path.name}")
    print(f"    Link Drive: {web_link}")
    return web_link


def main() -> None:
    parser = argparse.ArgumentParser(description="Tải ảnh minh chứng SMS lên Google Drive CS114")
    parser.add_argument("--file", type=str, help="Đường dẫn tới tệp ảnh đơn lẻ cần tải lên")
    parser.add_argument("--folder", type=str, help="Đường dẫn thư mục chứa nhiều ảnh chụp cần tải hàng loạt")
    parser.add_argument("--folder-id", type=str, default=DEFAULT_FOLDER_ID, help="ID thư mục Drive đích")
    parser.add_argument("--credentials", type=str, default=None, help="Đường dẫn tệp credentials.json tùy chọn")

    args = parser.parse_args()

    project_root = get_project_root()
    cred_file = Path(args.credentials) if args.credentials else project_root / "credentials.json"
    tok_file = project_root / "token.json"

    service = authenticate_google_drive(cred_file, tok_file)

    if args.file:
        link = upload_single_file(service, Path(args.file), args.folder_id)
        if link:
            print("\n" + "=" * 60)
            print("ĐƯỜNG LINK DÁN VÀO CỘT SOURCE_URL TRÊN GOOGLE SHEET:")
            print(link)
            print("=" * 60 + "\n")
        return

    if args.folder:
        folder_path = Path(args.folder)
        if not folder_path.is_dir():
            print(f"[!] Thư mục không tồn tại: {folder_path}")
            sys.exit(1)

        image_extensions = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}
        images = [f for f in folder_path.iterdir() if f.is_file() and f.suffix.lower() in image_extensions]

        if not images:
            print(f"[*] Không tìm thấy ảnh nào trong thư mục: {folder_path}")
            sys.exit(0)

        print(f"[*] Bắt đầu tải {len(images)} ảnh lên thư mục Drive ID: {args.folder_id}...")
        results = []
        for img in images:
            lnk = upload_single_file(service, img, args.folder_id)
            if lnk:
                results.append({"filename": img.name, "link": lnk})

        print(f"\n[+] ĐÃ HOÀN TẤT: Đã tải thành công {len(results)}/{len(images)} ảnh!")
        return

    print("[*] Kiểm tra kết nối Google Drive thành công!")
    print(f"[*] Để tải tệp, chạy: python3 drive_uploader.py --file <path_to_image>")


if __name__ == "__main__":
    main()
