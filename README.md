📦 HỆ THỐNG QUẢN LÝ KHO & ĐƠN HÀNG (Warehouse Management System)
🎓 Thông tin đồ án
Học phần: Phát triển ứng dụng Web
Loại bài: Thi kết thúc học phần
Nhóm thực hiện:
NGÔ THANH HOÀN
NGÔ MẠNH QUÂN
NGUYỄN CÔNG HOÀNG
1. 🚀 Giới thiệu hệ thống

Hệ thống được xây dựng nhằm hỗ trợ doanh nghiệp quản lý:

Sản phẩm trong kho
Đơn hàng
Trạng thái xử lý đơn
Người dùng hệ thống

Ứng dụng giúp tối ưu quy trình quản lý thủ công, giảm sai sót và tăng hiệu quả vận hành.

2. 🎯 Chức năng hệ thống
🔐 Quản lý người dùng
Đăng ký / Đăng nhập
Phân quyền cơ bản
📦 Quản lý sản phẩm
Thêm / sửa / xóa sản phẩm
Hiển thị danh sách sản phẩm
🧾 Quản lý đơn hàng
Tạo đơn hàng
Cập nhật trạng thái (Pending, Completed, Cancelled...)
Xem danh sách đơn
📊 Dashboard & Thống kê
Tổng số đơn hàng
Thống kê theo trạng thái
Biểu đồ trực quan
3. ⚙️ Công nghệ sử dụng
Backend: Django (Python 3)
Database: SQLite
Frontend: HTML, CSS, Django Template
Mô hình: MVC (Django MTV)
4. 🗄️ Thiết kế cơ sở dữ liệu

Hệ thống gồm ít nhất 5 bảng chính:

User (Django auth)
Product
Order
OrderItem
Category (hoặc tương đương)
🔗 Quan hệ:
Product → Category (Many-to-One)
Order → User (Many-to-One)
OrderItem → Order (Many-to-One)
OrderItem → Product (Many-to-One)

✔ Có sử dụng:

Primary Key
Foreign Key
Ràng buộc logic dữ liệu
5. 🖥️ Giao diện & UI/UX
Giao diện đơn giản, dễ sử dụng
Bố cục rõ ràng: Header – Menu – Content – Footer
Sử dụng base.html để tái sử dụng layout
Responsive cơ bản (hiển thị tốt trên nhiều màn hình)
6. 📈 Thống kê & báo cáo

Hệ thống hỗ trợ:

Thống kê số lượng đơn theo trạng thái
Hiển thị biểu đồ (Chart)
Dữ liệu được cập nhật theo thời gian thực
7. 🧪 Kiểm thử hệ thống

Đã thực hiện kiểm thử:

✅ CRUD sản phẩm
✅ CRUD đơn hàng
✅ Đăng nhập / đăng ký
✅ Kiểm tra luồng nghiệp vụ

Kết quả:

Hệ thống hoạt động ổn định
Không có lỗi nghiêm trọng
8. ▶️ Hướng dẫn cài đặt & chạy
Bước 1: Clone project
git clone <link_repo>
cd warehouse_full
Bước 2: Cài thư viện
pip install -r requirements.txt
Bước 3: Migrate database
python manage.py migrate
Bước 4: Chạy server
python manage.py runserver

👉 Truy cập: http://127.0.0.1:8000/

9. 🔑 Tài khoản test
Username: admin
Password: 123456
10. 🎥 Demo hệ thống
Video demo: (đính kèm link Google Drive / YouTube)
Thời lượng: 5–7 phút
Nội dung:
Đăng nhập
CRUD sản phẩm
Tạo đơn hàng
Xem dashboard
11. 📑 Tài liệu kèm theo
📘 Báo cáo PDF / DOCX
📊 Slide thuyết trình (10–15 trang)
📐 Sơ đồ:
ERD (Database)
Use Case
Kiến trúc hệ thống
12. 🌟 Tính năng mở rộng
Lọc sản phẩm nâng cao
Thống kê trực quan bằng biểu đồ
Có thể mở rộng:
Export Excel
API REST
AI gợi ý sản phẩm
