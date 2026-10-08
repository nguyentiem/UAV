# Drone từ gốc · Phần A–C

Mở `index.html` trong trình duyệt để học 22 bài: A1–A15 về toán, cơ học, khí động và mô hình; B1–B3 về PID và mã triển khai; C1–C4 về cảm biến, ước lượng tư thế, vòng kín và kiểm thử an toàn. Các trang hoạt động offline; hình là SVG hoặc canvas trong HTML, tương tác dùng JavaScript thuần. Không cần server hoặc quá trình build để **xem**.

## Cấu trúc

- `index.html`: mục lục.
- `A01.html`–`A15.html`, `B01.html`–`B03.html`, `C01.html`–`C04.html`: trang bài học riêng.
- `assets/`: giao diện và mô phỏng tương tác.
- `build.py`, `more_lessons.py`, `pid_lessons.py`, `c_lessons.py`: nguồn nội dung và trình tạo trang; chạy `python build.py` sau khi sửa nội dung.
- `examples/`: PID Python/C, mixer X, mô phỏng ba trục quay và kiểm tra.

Quy ước dùng xuyên suốt: world ENU (x Đông, y Bắc, z lên); body FLU (x mũi, y trái, z lên); `R` đổi vector body sang world. Motor X được đánh số 1 trước trái, 2 trước phải, 3 sau phải, 4 sau trái; 1/3 quay CCW khi nhìn từ trên.

A2 có mô phỏng tích vô hướng/tích có hướng, mô-men `r×F`, biến đổi mặt phẳng và phép xoay vector 3D. A4 dùng lại phép đổi body → world; A10 cho thay thrust từng motor để xem từng cột của ma trận mixer. Các mô phỏng này minh họa hình học và phép nhân ma trận, không ra lệnh phần cứng.

Ví dụ số là minh họa. Hệ số cánh quạt, quán tính, giới hạn motor và pin cần đo lại cho phần cứng cụ thể. Tài liệu Word ở thư mục cha được dùng làm nền nhập môn và đã được mở rộng theo đề cương A1–A15.

## Chạy ví dụ PID (PowerShell)

```powershell
cd drone-course/examples
python sim_cascade.py
python sim_position_hold.py
python -m unittest test_control.py
gcc -std=c11 -Wall -Wextra -pedantic pid.c flight_control.c test_flight_control.c -lm -o test_flight_control.exe
./test_flight_control.exe
```

`sim_cascade.py` ghi `attitude_step.csv` cho P góc 100 Hz và PID tốc độ góc 500 Hz. `sim_position_hold.py` ghi `position_step.csv` cho đủ 12 vòng: 3 P vị trí, 3 PID vận tốc, 3 P góc, 3 PID rate. Cả hai có mixer X và trễ motor; mã C triển khai vòng góc/rate. C1–C4 có mô phỏng cảm biến, complementary filter, vòng kín roll và logic arm/failsafe chạy trong trình duyệt. Các ví dụ Python/C chưa nối driver phần cứng, sensor fusion hay failsafe hoàn chỉnh.
