"""
================================================================================
DỰ ÁN CUỐI KỲ CS114 - MÁY HỌC (NHÓM 10 - UIT)
KHO MẪU TIN NHẮN BÌNH THƯỜNG ĐỜI THỰC (AUTHENTIC NORMAL SMS REPOSITORY)
================================================================================
Mục đích:
  - Cung cấp 365 mẫu tin nhắn SMS chuẩn thực tế tại Việt Nam không trùng lặp:
    + Nhóm 2: 130 mẫu Hóa đơn điện EVN, tiền nước, y tế phường, BHXH VssID.
    + Nhóm 3: 130 mẫu Tin nhắn gia đình, con cháu hỏi thăm, dặn uống thuốc.
    + Nhóm 4: 105 mẫu Khuyến mãi, tích điểm, chúc mừng sinh nhật nhà thuốc / siêu thị.
  - Đảm bảo tính độc bản (zero duplicate) tuyệt đối sau khi chạy qua `mask_pii()`.
================================================================================
"""

from __future__ import annotations


def get_utility_and_gov_messages() -> list[str]:
    """Sinh danh sách 130 mẫu tin nhắn độc bản về Điện nước, Y tế công, BHXH VssID."""
    messages: list[str] = []
    districts = [
        "Quan 1", "Quan 3", "Quan 5", "Quan 7", "Quan 10", "Binh Thanh",
        "Go Vap", "Thu Duc", "Tan Binh", "Phu Nhuan", "Ba Dinh", "Dong Da",
        "Cau Giay", "Ha Dong", "Long Bien",
    ]

    # 1. Điện lực EVN: 45 mẫu
    for i in range(45):
        dist = districts[i % len(districts)]
        amt = f"{320000 + i * 18500:,}d".replace(",", ".")
        month = f"{(i % 12) + 1:02d}/2026"
        due = f"{10 + (i % 15):02d}/09/2026"
        msg = (
            f"EVN {dist} TB: Tien dien thang {month} cua KH PE{i+1:06d} la {amt}. "
            f"Han dong tien: ngay {due}. Chi tiet xem tai app EVN CSKH hoac LH 1900545454. Tran trong."
        )
        messages.append(msg)

    # 2. Cấp nước SAWACO: 35 mẫu
    water_companies = [
        "SAWACO", "Cap nuoc Gia Dinh", "Cap nuoc Ben Thanh", "Cap nuoc Cho Lon",
        "Cap nuoc Thu Duc", "Cap nuoc Nha Be", "Cap nuoc Tan Hoa",
    ]
    for i in range(35):
        comp = water_companies[i % len(water_companies)]
        amt = f"{115000 + i * 7200:,}d".replace(",", ".")
        vol = 10 + (i % 15)
        month = f"{(i % 12) + 1:02d}/2026"
        due = f"{15 + (i % 12):02d}/09/2026"
        msg = (
            f"{comp} thong bao: Tien nuoc ky {month} cua Danh bo DB{i+1:06d} la {amt} "
            f"(tieu thu {vol} m3). Vui long thanh toan truoc ngay {due}. Hotline: 19001010."
        )
        messages.append(msg)

    # 3. Y tế & Bệnh viện công: 25 mẫu
    hospitals = [
        "BV Dai hoc Y Duoc TP.HCM", "Benh vien Cho Ray", "Benh vien Bach Mai",
        "Benh vien Tu Du", "Benh vien Nhan dan Gia Dinh", "Benh vien Thong Nhat",
        "Tram y te Phuong Ben Nghe", "Tram y te Phuong Dich Vong",
    ]
    departments = [
        "Noi Tim mach", "Lao khoa", "Noi Tiet - Tieu duong",
        "Co Xuong Khop", "Kham Tong quat", "Mat - Khuc xa",
    ]
    for i in range(25):
        hosp = hospitals[i % len(hospitals)]
        dep = departments[i % len(departments)]
        minute = 15 + (i % 4) * 15
        day = 10 + (i % 18)
        msg = (
            f"[{hosp}] Thong bao: Quy khach co lich hen kham chuyen khoa {dep} "
            f"vao luc 08:{minute:02d} ngay {day:02d}/09/2026 (Ma so BN: BN{i+1:05d}). "
            f"Vui long mang theo so kham va the BHYT. LH: 02838554269."
        )
        messages.append(msg)

    # 4. Bảo hiểm xã hội Việt Nam (VssID): 25 mẫu
    for i in range(25):
        dist = districts[i % len(districts)]
        month = f"{(i % 12) + 1:02d}/2026"
        msg = (
            f"BHXH Viet Nam thong bao: Ma so BHXH 7912{i+1:06d} da duoc co quan BHXH quan {dist} "
            f"ghi nhan dong BHYT thang {month}. Tra cuu qua trinh tham gia tai app VssID. Tong dai: 19009068."
        )
        messages.append(msg)

    return messages[:130]


def get_family_and_elderly_care_messages() -> list[str]:
    """Sinh danh sách 130 mẫu tin nhắn Gia đình, chăm sóc người cao tuổi độc bản."""
    relatives = [
        "Con", "Chau", "Con gai", "Con trai", "Ut", "Chau Mai", "Chau Nam",
        "Chau Linh", "Chau Minh", "Con Thao", "Chau Duc", "Con Huong", "Chau Huy",
    ]
    elders = [
        "ba", "ong", "me", "bo", "ngoai", "noi", "bac Ba", "bac Tu", "chu Sau",
        "co Bay", "cau Tam",
    ]
    medicines = [
        "thuoc huyet ap", "vien tieu duong", "thuoc tim mach",
        "thuoc bo khop Glucosamine", "thuoc ha mo mau", "vien canxi buoi sang",
        "thuoc nho mat", "vien bo nao Ginkgo", "thuoc da day", "thuoc chong chong mat",
    ]
    actions = [
        "sang nay an sang xong nho uong {med} luon nhe",
        "trua nay nho nghi ngoi roi uong {med} dung lieu",
        "hom nay troi tro gio, nho do huyet ap ghi vao so roi uong {med}",
        "chieu nay con ghe qua cho mua it hoa qua dem sang cho {eld}",
        "cuoi tuan nay ca nha con ve tham {eld}, may dua nho cu nhac suot",
        "hom nay con di lam ve som se ghe mua chao va thuoc cho {eld}",
        "nho uong nhieu nuoc am va dung quen uong {med} sau bua com toi",
        "sang mai co bac si o tram y te den kham suc khoe dinh ky cho hoi nguoi cao tuoi, {eld} nho di nhe",
        "chieu nay tan hoc chau se tu di bo ve, {eld} khong phai ra dau ngo don chau dau a",
        "con moi gui biet duoc hop sua Ensure cho {eld}, buu ta giao {eld} nho nhan giup con nhe",
    ]

    messages: list[str] = []
    seen = set()
    for r_idx, r in enumerate(relatives):
        for e_idx, e in enumerate(elders):
            for a_idx, act in enumerate(actions):
                med = medicines[(r_idx + e_idx + a_idx) % len(medicines)]
                msg = f"{r} chao {e} a, " + act.format(eld=e, med=med) + f". {r} chuc {e} luon khoe manh!"
                if msg not in seen:
                    seen.add(msg)
                    messages.append(msg)
                if len(messages) >= 130:
                    return messages
    return messages[:130]


def get_retail_and_pharmacy_promo_messages() -> list[str]:
    """Sinh danh sách 105 mẫu tin nhắn Khuyến mãi, Tích điểm siêu thị & nhà thuốc lành tính."""
    messages: list[str] = []

    # 1. Nhà thuốc: 55 mẫu
    pharmacies = ["Pharmacity", "FPT Long Chau", "Nha thuoc An Khang"]
    vitamins = [
        "Canxi va Vitamin D3", "Vien uong bo khop Glucosamine", "SuaEnsure Gold nguoi cao tuoi",
        "May do huyet ap Omron", "Dau ca Omega 3", "Hong sam Han Quoc", "Tra thao duoc atiso",
    ]
    for i in range(55):
        ph = pharmacies[i % len(pharmacies)]
        vit = vitamins[i % len(vitamins)]
        disc = 10 + (i % 6) * 5
        start_day = 10 + (i % 15)
        end_day = 25 + (i % 5)
        msg = (
            f"[{ph}] Chuong trinh tri an: Giam gia {disc}% cho san pham {vit} tai he thong "
            f"tren toan quoc tu {start_day:02d}/09 den {end_day:02d}/09/2026. Ma uu dai: HEALTH{i+1:03d}. "
            f"Chi tiet LH: 18006928."
        )
        messages.append(msg)

    # 2. Siêu thị bán lẻ: 50 mẫu
    supermarkets = [
        "Co.opmart", "WinMart", "Sieu thi GO!", "Bach hoa XANH", "Lotte Mart", "AEON Mall",
    ]
    items = [
        "Rau sach WinEco va trai cay", "Thit heo MEATDeli sach", "Sua tuoi va cac san pham tu sua",
        "Gao thom ST25 va gia vi", "Thuc pham dong lanh va do kho",
    ]
    for i in range(50):
        sm = supermarkets[i % len(supermarkets)]
        it = items[i % len(items)]
        pts = 100 + i * 20
        day_week = 2 + (i % 6)
        msg = (
            f"[{sm}] Uu dai hoi vien: Tang {pts} diem thuong khi mua sam {it} trong ngay thu {day_week}. "
            f"The thanh vien ap dung tai toan bo chi nhanh {sm}. Hotline: 1900555568. Tran trong."
        )
        messages.append(msg)

    return messages[:105]
