
## 1. Mô tả dự án
Ứng dụng web cho phép người dùng:
- Quản lý sản phẩm trong kho
- Quản lý đơn hàng
- Theo dõi trạng thái đơn hàng
- Đăng nhập, đăng ký tài khoản người dùng

## 2. Chức năng chính
- Đăng nhập / Đăng ký người dùng
- CRUD sản phẩm (Thêm, sửa, xóa, xem)
- CRUD đơn hàng
- Thống kê đơn hàng theo trạng thái
- Dashboard quản lý
- Menu điều hướng, header, footer thống nhất
- Template inheritance (base.html)

## 3. Công nghệ sử dụng
- Python 3
- Django
- SQLite (CSDL mặc định)
- HTML, CSS (Template Django)

## 4. Cấu trúc thư mục chính
warehouse_full/
│
├── accounts/
├── inventory/
├── templates/
│ ├── accounts/
│ └── inventory/
├── config/
├── db.sqlite3
├── manage.py
├── README.md
└── requirements.txt

## 5. Cài đặt môi trường

### Bước 1: Clone hoặc tải project
git clone <link_repo>
Hoặc tải file zip và giải nén.

### Bước 2: Cài thư viện
pip install -r requirements.txt

Hoặc:
pip install django


### Bước 3: Chạy migrate
python manage.py migrate


### Bước 4: Tạo tài khoản admin (tuỳ chọn)
python manage.py createsuperuser


### Bước 5: Chạy server
python manage.py runserver

Truy cập trình duyệt:
http://127.0.0.1:8000/
Link GitHub : https://github.com/dtc235200292-star/warehouse_full

## 6. Tài khoản mẫu (nếu có)
- Username: admin  
- Password: 123456  
(Hoặc tự tạo bằng createsuperuser)


## 7. Seed data
Hệ thống có dữ liệu mẫu để hiển thị danh sách sản phẩm và đơn hàng.


## 8. Giao diện
- Trang Home
- Trang Login
- Trang Register
- Trang Dashboard
- Trang CRUD sản phẩm
- Trang CRUD đơn hàng


## 9. Template inheritance
Sử dụng `base.html` làm layout chung:
- Header
- Menu
- Footer
Các trang kế thừa từ `base.html` bằng `{% extends 'base.html' %}`.


## 10. Hướng dẫn test nhanh
1. Đăng ký tài khoản
2. Đăng nhập
3. Thêm sản phẩm
4. Tạo đơn hàng
5. Kiểm tra danh sách và thống kê

## 11. Tác giả
-NGÔ THANH HOÀN 
-NGÔ MẠNH QUÂN
-NGUYỄN CÔNG HOÀNG 

## 12. Ghi chú
- Sử dụng SQLite để dễ chạy trên mọi máy
- Có thể chuyển sang MySQL/PostgreSQL nếu cần
update step 1
update step 2
