@echo off
chcp 65001 >nul
set PYTHONIOENCODING=utf-8
title He Thong Phat Hien Tin Nhan Lua Dao - CS114 Nhom 10

echo ======================================================================
echo    HỆ THỐNG PHÁT HIỆN TIN NHẮN LỪA ĐẢO CHO NGƯỜI CAO TUỔI (CS114)
echo ======================================================================
echo.
echo [*] Đang khởi động ứng dụng Web...
echo [*] Trình duyệt web sẽ tự động mở trang kiểm tra ngay bây giờ...
echo [*] (Khi nào muốn tắt ứng dụng, chỉ cần đóng cửa sổ này lại nhé)
echo.

cd /d "%~dp0draft\scam-detection"
python -m streamlit run demo\app.py

pause
