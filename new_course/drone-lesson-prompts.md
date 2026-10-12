# Bộ prompt viết bài học HTML – Giáo án Drone Quadcopter

## Cách dùng

1. Mở một cuộc trò chuyện mới với ChatGPT, dán **PROMPT NỀN** (bên dưới) và gửi. Prompt này đặt quy chuẩn chung về giao diện, cấu trúc và kỹ thuật.
2. Với mỗi bài, dán **prompt của bài đó** trong cùng cuộc trò chuyện. ChatGPT sẽ áp dụng quy chuẩn nền và chỉ cần nội dung riêng của bài.
3. Sau bài đầu tiên ưng ý, yêu cầu: "Giữ nguyên toàn bộ CSS và bảng màu của bài trước cho các bài sau" để các bài đồng nhất.
4. Nếu câu trả lời bị cắt ngắn, gửi: "Tiếp tục từ đoạn code bị cắt, không lặp lại phần đã viết".
5. Công thức và mô phỏng do AI viết có thể sai dấu hoặc hệ số. Hãy đối chiếu với sách (Beard, Mellinger & Kumar, tài liệu PX4/ArduPilot) trước khi dùng.

## Lộ trình

| Giai đoạn | Bài | Nội dung |
|---|---|---|
| 1. Lý thuyết | 1–7 | Hệ tọa độ, lực và mô men, toán nền, động lực học, IMU, điều khiển, ước lượng trạng thái |
| 2. Mô phỏng | 8–12 | Mô phỏng 6-DOF, PID attitude, cảm biến + EKF, PX4 SITL, quỹ đạo |
| 3. Thực nghiệm | 13–16 | Phần cứng và firmware, bench test, giàn thử và tuning, bay thật |
| 4. Hoàn thiện | 17 | Nhận dạng hệ thống và mở rộng |

---

## PROMPT NỀN (gửi một lần ở đầu cuộc trò chuyện)

````
Bạn là giảng viên kỹ thuật kiêm lập trình viên front-end giàu kinh nghiệm. Tôi đang xây dựng một giáo án học và phát triển drone quadcopter, đi từ lý thuyết toán/vật lý đến mô phỏng và thực nghiệm. Mỗi lần tôi gửi nội dung một bài, hãy viết bài đó thành MỘT FILE HTML DUY NHẤT (HTML + CSS + JavaScript thuần, mở bằng trình duyệt là chạy).

ĐỐI TƯỢNG: kỹ sư embedded đã quen lập trình C, STM32 và FreeRTOS, mới học về drone. Ngôn ngữ bài học: tiếng Việt, giữ thuật ngữ tiếng Anh trong ngoặc khi cần.

GIAO DIỆN
- Giao diện sáng, thanh lịch, nhẹ nhàng: nền trắng ngà hoặc xám rất nhạt, màu nhấn xanh pastel/xanh ngọc dịu, chữ xám đậm (không dùng đen tuyền, không dùng màu chói).
- Nhiều khoảng trắng, bo góc, đổ bóng nhẹ, bố cục dạng thẻ (card).
- Font dễ đọc (Google Fonts, có fallback), dãn dòng thoải mái.
- Mục lục cố định (sidebar hoặc thanh trên) có highlight mục đang đọc và cuộn mượt.
- Responsive cho điện thoại và máy tính.
- Dùng biến CSS (:root) cho toàn bộ bảng màu.
- Công thức toán dùng KaTeX hoặc MathJax (CDN).
- Code mẫu có tô màu cú pháp và nút Copy.

CẤU TRÚC MỖI BÀI (theo thứ tự)
1. Mở đầu: bài giải quyết vấn đề gì, vì sao quan trọng, kiến thức cần có trước, sơ đồ tổng quan.
2. Lý thuyết chi tiết: đi từ trực giác đến công thức. Mỗi khái niệm gồm định nghĩa bằng lời dễ hiểu, công thức kèm ý nghĩa và đơn vị từng đại lượng, ví dụ số có lời giải từng bước, hộp "Lưu ý / Sai lầm thường gặp".
   - Trước khi dùng vector, ma trận, chuyển vị/nghịch đảo hay phép quay, phải có bài nền hoặc liên kết rõ tới phần dạy các phép toán đó; không giả định người học đã biết đại số tuyến tính.
   - Mỗi mục lý thuyết phải giải thích chuỗi: hiện tượng thực → giả thiết → suy ra công thức → ý nghĩa vật lý và đơn vị → miền áp dụng/giới hạn → ví dụ số được kiểm tra. Không thay bài giảng bằng danh sách ý hoặc một công thức đơn lẻ.
3. Hình ảnh trực quan: vẽ bằng SVG hoặc Canvas ngay trong file (không dùng ảnh ngoài), có chú thích rõ ràng.
   - Mỗi bài cần hình riêng cho cơ chế chính và một hình riêng cho quan hệ định lượng hoặc luồng xử lý. Hình phải có nhãn trục, chiều dương, đơn vị và chú giải; không tái dùng một biểu đồ dao động chung cho các chủ đề khác nhau.
4. Mô phỏng animation: ít nhất 1–2 animation (requestAnimationFrame) có nút Play/Pause/Reset.
5. Phòng thí nghiệm tương tác: thanh trượt, ô nhập, nút bấm để đổi tham số và thấy kết quả theo thời gian thực qua hình vẽ, biểu đồ và số liệu; hiển thị công thức đang tính bên cạnh.
6. Hướng dẫn thực hành từng bước: các bước đánh số, mỗi bước nêu mục tiêu, cách làm, kết quả mong đợi, cách kiểm tra đúng/sai; kèm code mẫu hoàn chỉnh có chú thích.
7. Lỗi thường gặp: bảng "Hiện tượng → Nguyên nhân → Cách xử lý".
8. Bài tập tự kiểm tra: 3 mức (cơ bản, vận dụng, nâng cao); đáp án ẩn, bấm "Xem đáp án" mới hiện, có lời giải chi tiết.
9. Tóm tắt các ý chính và liên hệ với bài tiếp theo.

KỸ THUẬT
- Một file .html duy nhất; thư viện ngoài chỉ nạp qua CDN (KaTeX/MathJax, highlight.js, Chart.js nếu cần).
- Code sạch, chia section rõ, có comment.
- Animation mượt (~60fps), tôn trọng prefers-reduced-motion.
- Mô phỏng phải đúng về vật lý/toán học; nếu đơn giản hóa thì ghi rõ trong bài.
- Không để chỗ trống kiểu "tự hoàn thiện sau" hoặc "..."; mọi tính năng phải chạy được.

CÁCH TRẢ LỜI
- Trước code: tóm tắt cấu trúc bài trong 3–5 dòng.
- Toàn bộ code trong MỘT khối duy nhất, không cắt ngắn. Nếu quá dài, chia thành các phần liên tiếp và nói rõ cách ghép.
- Sau code: nêu cách chạy và 3 gợi ý mở rộng.

Nếu đã hiểu, hãy trả lời "Sẵn sàng" và chờ nội dung bài đầu tiên.
````

---

# GIAI ĐOẠN 1: CƠ SỞ LÝ THUYẾT

## Bài 1 – Tổng quan quadcopter, hệ tọa độ và bậc tự do

````
BÀI 1: Tổng quan quadcopter, hệ tọa độ và bậc tự do

Mục tiêu: hiểu quadcopter gồm những khối nào, vì sao 4 động cơ đủ để điều khiển 6 bậc tự do, và phân biệt được các hệ tọa độ.
Kiến thức cần có: vật lý phổ thông, đại số cơ bản.

Nội dung lý thuyết bắt buộc:
- Các khối của drone: khung, động cơ BLDC, ESC, cánh quạt, pin LiPo, flight controller, IMU, bộ thu RC; sơ đồ khối luồng tín hiệu.
- Cấu hình X và +, chiều quay từng động cơ (CW/CCW) và lý do phải xen kẽ.
- Hệ tọa độ world (NED/ENU) và body; quy ước trục, chiều dương roll/pitch/yaw.
- 6 bậc tự do và hiện tượng "underactuated" (4 đầu vào, 6 bậc tự do).
- Bốn lệnh điều khiển cơ bản: throttle, roll, pitch, yaw và tác động lên 4 động cơ (giới thiệu trực giác, chưa cần công thức).

Hình ảnh SVG: drone nhìn từ trên xuống và nhìn nghiêng, gắn nhãn động cơ 1–4 kèm chiều quay; hai hệ trục world và body.
Animation: drone 3D giả lập (SVG/Canvas) tự xoay roll, pitch, yaw theo từng lệnh để thấy ý nghĩa các góc.
Phòng thí nghiệm tương tác: 4 thanh trượt tốc độ động cơ, drone phản ứng (nghiêng/xoay/nâng) theo chênh lệch tốc độ, hiển thị mô tả chuyển động bằng chữ.
Thực hành: bài tập quan sát, không cần phần cứng; có code Python nhỏ in ra bảng "động cơ nào tăng thì drone chuyển động thế nào".
Lỗi thường gặp: nhầm chiều dương các trục, nhầm chiều quay động cơ và chiều cánh quạt.
Bài tập: xác định hướng chuyển động khi tăng/giảm các cặp động cơ; chuyển đổi tọa độ NED ↔ ENU.
````

## Bài 2 – Lực nâng, mô men xoắn và ma trận mixer

````
BÀI 2: Lực nâng, mô men xoắn và ma trận mixer

Mục tiêu: hiểu động cơ quay tạo ra lực nâng và mô men phản lực như thế nào, và tự dựng được ma trận mixer.
Kiến thức cần có: Bài 1; lực, mô men, đạo hàm cơ bản.

Nội dung lý thuyết bắt buộc (nhiều vật lý và toán, giải thích từ nguyên lý):
- Các lực tác động lên drone: trọng lực, tổng lực nâng, lực cản không khí; điều kiện hover.
- Cánh quạt tạo lực nâng: nguyên lý động lượng (momentum theory), giải thích T = k_T·ω² và Q = k_Q·ω²; ý nghĩa và đơn vị k_T, k_Q; tại sao lực nâng tỷ lệ với bình phương tốc độ.
- Mô men phản lực làm drone xoay yaw; vì sao cần 2 động cơ CW và 2 CCW.
- Mô men roll/pitch sinh ra từ chênh lệch lực nâng nhân với cánh tay đòn (khoảng cách động cơ đến tâm).
- Dựng ma trận mixer: quan hệ [T, τ_x, τ_y, τ_z] = M·[ω1², ω2², ω3², ω4²] cho cấu hình X và +; nghịch đảo ma trận để từ lệnh điều khiển ra tốc độ động cơ.
- Ví dụ số hoàn chỉnh: drone 1.2 kg, cánh tay đòn 0.25 m, tính throttle hover.
- Giới hạn thực tế: bão hòa động cơ, ưu tiên khi vượt giới hạn.

Hình ảnh SVG: sơ đồ lực/mô men trên từng động cơ, mũi tên tỷ lệ theo ω; hình minh họa luồng không khí qua cánh quạt.
Animation: 4 cánh quạt quay với tốc độ theo ω, mũi tên lực nâng và mô men thay đổi theo thời gian thực.
Phòng thí nghiệm tương tác: chỉnh k_T, k_Q, khối lượng, cánh tay đòn; hiển thị ma trận mixer và ma trận nghịch đảo cập nhật trực tiếp; nhập (T, τ_x, τ_y, τ_z) để nhận ra ω1..ω4, cảnh báo khi vượt giới hạn.
Thực hành: viết hàm mixer bằng Python (numpy) và bản C (không dùng thư viện) chạy trên STM32; kiểm thử với các trường hợp hover, roll, yaw thuần.
Lỗi thường gặp: nhầm dấu mô men yaw, quên bình phương ω, dùng sai cấu hình X/+.
Bài tập: tính lực nâng cực đại và tỷ số lực đẩy/trọng lượng; thiết kế mixer cho hexacopter.
````

## Bài 3 – Toán nền: vector, ma trận quay, góc Euler và quaternion

````
BÀI 3: Toán nền cho điều khiển drone: vector, ma trận quay, góc Euler và quaternion

Mục tiêu: biểu diễn và biến đổi hướng (attitude) của drone, hiểu gimbal lock và vì sao dùng quaternion.
Kiến thức cần có: Bài 1; đại số tuyến tính cơ bản.

Nội dung lý thuyết bắt buộc:
- Vector, tích vô hướng, tích có hướng (liên hệ với mô men = r × F); ma trận skew-symmetric.
- Ma trận quay quanh từng trục; tính chất (trực chuẩn, det = 1); quay hợp thành và tính không giao hoán.
- Góc Euler Z-Y-X (yaw-pitch-roll), ma trận quay tổng hợp body → world; gimbal lock và minh họa.
- Quaternion: định nghĩa, phép nhân, liên hợp, chuẩn hóa, quay vector bằng quaternion, chuyển đổi qua lại với ma trận quay và Euler.
- Quan hệ giữa vận tốc góc ω (gyro) và đạo hàm của góc Euler/quaternion; tích phân quaternion.
- Ví dụ số từng bước cho mỗi phép biến đổi.

Hình ảnh SVG/Canvas: khối hộp 3D (drone đơn giản) quay theo ma trận, hiển thị ba trục body so với world.
Animation: demo gimbal lock (pitch = 90° làm mất một bậc tự do) so với quaternion; demo nội suy quaternion (SLERP).
Phòng thí nghiệm tương tác: thanh trượt roll/pitch/yaw, hiển thị đồng thời ma trận quay, quaternion tương ứng, và hình 3D; ô nhập quaternion để xem Euler; nút tích phân vận tốc góc nhập tay.
Thực hành: viết thư viện nhỏ Python rồi C (chuyển đổi Euler ↔ quaternion ↔ ma trận, nhân quaternion, chuẩn hóa) và các bước kiểm thử đơn vị (unit test).
Lỗi thường gặp: nhầm thứ tự quay, quên chuẩn hóa quaternion, nhầm quy ước Hamilton/JPL.
Bài tập: quay vector bằng hai cách rồi so sánh; tìm Euler từ quaternion đã cho.
````

## Bài 4 – Động lực học 6-DOF: phương trình Newton–Euler

````
BÀI 4: Động lực học quadcopter 6-DOF: phương trình Newton–Euler

Mục tiêu: tự viết được mô hình toán học đầy đủ của quadcopter ở dạng phương trình trạng thái.
Kiến thức cần có: Bài 2 và Bài 3.

Nội dung lý thuyết bắt buộc:
- Phương trình tịnh tiến (Newton) trong hệ world: m·a = R·[0, 0, −T]ᵀ + m·g + lực cản.
- Phương trình quay (Euler) trong hệ body: I·ω̇ = τ − ω × (I·ω); giải thích số hạng con quay (gyroscopic) và ma trận quán tính I.
- Phương trình động học: đạo hàm vị trí, vận tốc, quaternion.
- Vector trạng thái 13 phần tử (p, v, q, ω) và cách đóng gói thành ẋ = f(x, u).
- Tuyến tính hóa quanh điểm hover: hệ rút gọn cho roll, pitch, yaw, độ cao (các hàm truyền dạng tích phân kép).
- Tích phân số: Euler, RK2, RK4; so sánh sai số, bước thời gian.
- Ví dụ số: dẫn xuất mô hình cho drone có thông số cụ thể.

Hình ảnh SVG: sơ đồ khối từ 4 lệnh động cơ → lực/mô men → gia tốc → vận tốc → vị trí; hình mô tả các đại lượng trong hệ world/body.
Animation: drone mô phỏng chuyển động tự do với điều kiện đầu và lực/mô men nhập vào; vẽ quỹ đạo.
Phòng thí nghiệm tương tác: chỉnh khối lượng, ma trận quán tính, lực cản, bước thời gian, chọn phương pháp Euler/RK4 và quan sát sai số tích lũy; đồ thị trạng thái theo thời gian.
Thực hành: cài đặt hàm f(x, u) và bộ tích phân RK4 bằng Python từng bước; kiểm tra bằng các trường hợp đã biết (rơi tự do, hover cân bằng, quay đều).
Lỗi thường gặp: nhầm hệ tọa độ giữa các phương trình, bước thời gian quá lớn làm mô phỏng phân kỳ.
Bài tập: tuyến tính hóa và tìm hàm truyền roll; ước lượng tần số dao động của mô hình.
````

## Bài 5 – Cảm biến IMU và nhiễu

````
BÀI 5: Cảm biến quán tính (IMU), mô hình nhiễu và hiệu chuẩn

Mục tiêu: hiểu cảm biến đo gì, sai số của chúng ra sao và tại sao không thể tin trực tiếp vào một cảm biến.
Kiến thức cần có: Bài 3; xác suất cơ bản (trung bình, phương sai).

Nội dung lý thuyết bắt buộc:
- Gyroscope MEMS, accelerometer, magnetometer, barometer: nguyên lý, đại lượng đo, đơn vị, tần số lấy mẫu điển hình.
- Mô hình sai số: bias, scale factor, noise, bias instability, drift; mật độ nhiễu và Allan variance (ở mức khái niệm).
- Accelerometer đo specific force (không phải gia tốc thuần): vì sao hover cho ra +1g.
- Từ accelerometer tính roll/pitch tĩnh, từ magnetometer tính yaw; hạn chế khi drone rung và khi có nhiễu từ.
- Nhiễu rung động từ động cơ, lọc thông thấp, lọc notch, ảnh hưởng của độ trễ lọc lên vòng điều khiển.
- Hiệu chuẩn: bias gyro khi đứng yên, hiệu chuẩn 6 mặt accelerometer, hiệu chuẩn mag (hard/soft iron).
- Ví dụ số: tích phân gyro có bias 0.5°/s trong 60 giây gây lệch bao nhiêu.

Hình ảnh SVG: sơ đồ mô tả MEMS gyro/accel; đồ thị phổ nhiễu minh họa.
Animation: tín hiệu cảm biến giả lập (thật + nhiễu + bias) chạy theo thời gian, thấy rõ drift khi tích phân gyro.
Phòng thí nghiệm tương tác: chỉnh nhiễu, bias, tần số rung, tần số cắt bộ lọc thông thấp, xem tín hiệu trước và sau lọc cùng độ trễ pha.
Thực hành: viết code C đọc IMU qua SPI/I²C trên STM32 (khung driver, cấu hình ODR, đọc FIFO/DMA), quy trình hiệu chuẩn bias; log dữ liệu ra UART và vẽ bằng Python.
Lỗi thường gặp: sai đơn vị, sai trục lắp, đọc dữ liệu chưa sẵn sàng, aliasing do lấy mẫu thấp.
Bài tập: tính độ trôi góc theo thời gian; chọn tần số cắt bộ lọc hợp lý.
````

## Bài 6 – Lý thuyết điều khiển và PID

````
BÀI 6: Lý thuyết điều khiển cơ bản và bộ điều khiển PID

Mục tiêu: hiểu phản hồi, tính ổn định và thiết kế được PID cho trục roll/pitch/yaw.
Kiến thức cần có: Bài 4 (hàm truyền dạng tích phân kép), số phức cơ bản.

Nội dung lý thuyết bắt buộc:
- Hệ vòng hở và vòng kín, sai số, phản hồi âm.
- Đáp ứng bước: thời gian lên, vọt lố, thời gian xác lập, sai số xác lập.
- Ổn định: cực của hệ thống, mặt phẳng s, quỹ đạo nghiệm số (root locus) ở mức trực giác; biên độ và biên pha.
- PID: vai trò của P, I, D; tác động khi tăng/giảm từng hệ số; phương trình rời rạc hóa.
- Vấn đề thực tế: tích phân bão hòa (anti-windup), nhiễu khuếch đại bởi D (lọc đạo hàm, derivative on measurement), giới hạn đầu ra.
- Cascade control: vòng trong tốc độ góc, vòng ngoài góc; vì sao vòng trong phải nhanh hơn 4–10 lần.
- Phương pháp chỉnh định: Ziegler–Nichols và cách tuning thủ công theo thứ tự P → D → I.
- Ví dụ số: PID cho plant tích phân kép, tính đáp ứng.

Hình ảnh SVG: sơ đồ khối vòng điều khiển cascade; đồ thị đáp ứng bước với các thông số được chú thích.
Animation: một thanh/con lắc (hoặc drone 1 trục) cân bằng bằng PID, có thể đẩy nhiễu bằng chuột.
Phòng thí nghiệm tương tác: chỉnh Kp, Ki, Kd, bật/tắt anti-windup, lọc D, độ trễ; xem đáp ứng bước, sai số và tín hiệu điều khiển; nút "Nhiễu xung" và "Nhiễu hằng".
Thực hành: cài đặt PID rời rạc bằng C (struct, hàm update, anti-windup, giới hạn) chạy trong task FreeRTOS 1 kHz; so sánh với phiên bản Python.
Lỗi thường gặp: dt không cố định, D khuếch đại nhiễu, I tích lũy khi chưa cất cánh, đảo dấu phản hồi.
Bài tập: tune PID cho plant cho trước theo yêu cầu vọt lố < 10%; giải thích dao động xuất hiện khi tăng Kd quá mức.
````

## Bài 7 – Ước lượng trạng thái: bộ lọc bổ sung và Kalman

````
BÀI 7: Ước lượng trạng thái: complementary filter, Madgwick/Mahony, Kalman và EKF

Mục tiêu: kết hợp gyro, accel, mag để ước lượng hướng (attitude) ổn định và chính xác.
Kiến thức cần có: Bài 3, 5, 6; xác suất cơ bản (phân phối Gauss, hiệp phương sai).

Nội dung lý thuyết bắt buộc:
- Vì sao cần hợp nhất cảm biến: gyro mượt nhưng trôi, accel không trôi nhưng nhiễu.
- Complementary filter: công thức, hằng số thời gian, giải thích tần số cắt bằng trực giác.
- Mahony và Madgwick: ý tưởng hiệu chỉnh quaternion bằng sai số hướng trọng lực; vai trò của các hệ số.
- Kalman filter tuyến tính: dự báo/cập nhật, hiệp phương sai trạng thái, Kalman gain; ví dụ 1 chiều với số liệu.
- EKF cho attitude: tuyến tính hóa mô hình phi tuyến, ma trận Jacobian, Q và R ảnh hưởng thế nào.
- Ước lượng bias gyro như một biến trạng thái.
- So sánh: độ chính xác, chi phí tính toán trên MCU, độ khó chỉnh tham số.

Hình ảnh SVG: sơ đồ khối từng bộ lọc; hình minh họa phân bố Gauss trước/sau cập nhật.
Animation: tín hiệu gyro (trôi), accel (nhiễu), kết quả lọc so với góc thật, chạy liên tục.
Phòng thí nghiệm tương tác: chỉnh hệ số bộ bổ sung, Madgwick beta, Q, R của Kalman; kích thích bằng chuyển động mô phỏng (nghiêng, rung, gia tốc ngang) và xem sai số của từng bộ lọc cạnh nhau.
Thực hành: cài đặt Mahony hoặc Madgwick bằng C (chạy 1 kHz trên STM32, ước lượng thời gian thực thi), cài đặt EKF tối giản bằng Python.
Lỗi thường gặp: gia tốc ngang bị hiểu nhầm là nghiêng, Q/R chọn sai khiến bộ lọc chậm hoặc nhiễu, quên chuẩn hóa quaternion.
Bài tập: giải thích vì sao tăng hệ số tin accel làm drone nhạy với rung; chọn Q, R hợp lý cho dữ liệu cho trước.
````

---

# GIAI ĐOẠN 2: MÔ PHỎNG

## Bài 8 – Xây dựng bộ mô phỏng drone 6-DOF bằng Python

````
BÀI 8: Xây dựng bộ mô phỏng drone 6-DOF bằng Python từ đầu

Mục tiêu: tự cài đặt mô hình động lực học Bài 4 thành chương trình mô phỏng hoàn chỉnh.
Kiến thức cần có: Bài 2, 3, 4; Python và numpy.

Nội dung bắt buộc:
- Cấu trúc chương trình: lớp Drone (tham số, trạng thái), hàm đạo hàm, bộ tích phân RK4, vòng lặp mô phỏng, ghi log.
- Mô hình động cơ có độ trễ (bậc nhất) và bão hòa; mô hình cản không khí đơn giản.
- Kiểm tra tính đúng đắn: bảo toàn năng lượng ở trường hợp lý tưởng, so khớp với nghiệm giải tích (rơi tự do, hover).
- Hiển thị: đồ thị trạng thái và hoạt hình 3D bằng matplotlib.
- Giải thích cách chọn bước thời gian và cách kiểm tra phân kỳ.

Hình ảnh SVG: sơ đồ lớp/luồng dữ liệu của chương trình mô phỏng.
Animation (JS): bản demo trực quan của chính mô hình này chạy trong trình duyệt, cho phép nhập lực/mô men và xem quỹ đạo.
Phòng thí nghiệm tương tác: chỉnh khối lượng, quán tính, độ trễ động cơ, cản; xem tác động lên đáp ứng khi cho lệnh bước.
Thực hành: hướng dẫn từng bước kèm code Python hoàn chỉnh (chia thành các file/hàm nhỏ), mỗi bước có kết quả mong đợi và cách kiểm tra.
Lỗi thường gặp: ma trận quán tính sai, quaternion không chuẩn hóa sau tích phân, đơn vị lẫn lộn.
Bài tập: thêm gió ngẫu nhiên; thêm hiệu ứng ground effect đơn giản.
````

## Bài 9 – Điều khiển góc (attitude) bằng cascade PID trong mô phỏng

````
BÀI 9: Điều khiển góc (attitude) bằng cascade PID trong mô phỏng

Mục tiêu: làm drone mô phỏng bay hover ổn định và đáp ứng lệnh góc.
Kiến thức cần có: Bài 6, 7, 8.

Nội dung bắt buộc:
- Kiến trúc controller: vòng ngoài (sai số góc → tốc độ góc mong muốn), vòng trong (tốc độ góc → mô men), mixer, giới hạn.
- Sai số hướng bằng quaternion (tránh cộng trừ góc Euler gây sai ở vùng biên).
- Điều khiển độ cao (throttle) và yaw.
- Quy trình tuning mô phỏng từng bước: vòng trong trước, rồi vòng ngoài.
- Đánh giá bằng chỉ số: vọt lố, thời gian xác lập, sai số, mức dùng động cơ.
- Kiểm tra độ bền (robustness): thay đổi khối lượng, nhiễu, trễ.

Hình ảnh SVG: sơ đồ khối controller đầy đủ.
Animation: drone bám theo chuỗi lệnh góc, hiển thị góc mong muốn và góc thực song song.
Phòng thí nghiệm tương tác: chỉnh các hệ số PID hai vòng, chọn dạng nhiễu, xem đồ thị và các chỉ số tự động tính.
Thực hành: code Python hoàn chỉnh nối controller với bộ mô phỏng Bài 8, kịch bản kiểm thử (hover, bước góc, nhiễu xung); hướng dẫn quan sát và rút kinh nghiệm khi mất ổn định.
Lỗi thường gặp: vòng trong chậm hơn vòng ngoài, bão hòa động cơ gây mất ổn định, dấu sai trong mixer.
Bài tập: tìm hệ số tối ưu bằng tìm kiếm lưới; so sánh PID với P-only ở vòng ngoài.
````

## Bài 10 – Mô phỏng cảm biến và tích hợp bộ ước lượng

````
BÀI 10: Mô phỏng cảm biến và tích hợp bộ ước lượng vào vòng điều khiển

Mục tiêu: chạy controller bằng trạng thái ước lượng (không phải trạng thái thật), như drone thật.
Kiến thức cần có: Bài 5, 7, 9.

Nội dung bắt buộc:
- Mô hình cảm biến giả lập: IMU có nhiễu, bias, tần số lấy mẫu rời rạc, độ trễ; baro, GPS (mức khái niệm).
- Chạy nhiều tần số: vật lý 1 kHz, IMU 1 kHz, controller 500 Hz–1 kHz, GPS 5–10 Hz.
- Tích hợp complementary/Madgwick/EKF; so sánh chất lượng bay với dùng trạng thái lý tưởng.
- Phân tích tác động của độ trễ và nhiễu lên ổn định.
- Cách thiết kế để dễ chuyển nguyên bộ controller+estimator sang C trên MCU.

Hình ảnh SVG: sơ đồ luồng dữ liệu: plant → cảm biến → estimator → controller → mixer → plant.
Animation: so sánh drone "thật" và drone "ước lượng" cạnh nhau, vẽ sai số theo thời gian.
Phòng thí nghiệm tương tác: chỉnh nhiễu, bias, độ trễ, tần số cắt lọc, chọn loại estimator; xem chất lượng bay thay đổi.
Thực hành: code Python mở rộng từ Bài 8–9, kèm kịch bản kiểm thử, hướng dẫn ghi log định dạng CSV để dùng lại cho bài sau.
Lỗi thường gặp: hiểu sai khung thời gian giữa các luồng, dùng trạng thái thật vô tình trong controller.
Bài tập: tìm mức nhiễu IMU tối đa mà drone còn hover được.
````

## Bài 11 – Mô phỏng hệ thống đầy đủ với PX4/ArduPilot SITL và Gazebo

````
BÀI 11: PX4/ArduPilot SITL và Gazebo: hiểu kiến trúc flight stack thật

Mục tiêu: chạy được flight stack thực trong mô phỏng và đọc hiểu kiến trúc của nó.
Kiến thức cần có: Bài 9, 10; Linux cơ bản.

Nội dung bắt buộc:
- Khái niệm SITL/HITL, vai trò của simulator (Gazebo/jMAVSim), cầu nối MAVLink.
- Kiến trúc PX4 (module, uORB, EKF2, mc_att_control, mc_pos_control, mixer/control allocator) và so sánh với ArduPilot (nêu tương đồng/khác biệt).
- Các chế độ bay: Manual/Stabilized, Altitude, Position, Mission; failsafe.
- Đọc log (ulog/flight review hoặc ArduPilot logs) và phân tích tracking, rung động.
- Cách liên hệ từng module với phần tự viết ở Bài 8–10.

Hình ảnh SVG: sơ đồ kiến trúc PX4 và luồng dữ liệu giữa các module, chú thích liên hệ với bài trước.
Animation: sơ đồ động minh họa tin nhắn đi giữa simulator, flight stack và QGroundControl.
Phòng thí nghiệm tương tác: bảng tham số quan trọng (MC_ROLLRATE_P, MC_PITCH_P...), mô phỏng đơn giản tác dụng khi chỉnh để người học hiểu ý nghĩa.
Thực hành: các bước cài đặt môi trường (Ubuntu/WSL), build PX4 SITL, chạy Gazebo, kết nối QGroundControl, bay mission thử, đổi tham số và so sánh log; có bảng xử lý lỗi cài đặt thường gặp.
Lỗi thường gặp: thiếu dependency, sai phiên bản Gazebo, không kết nối được MAVLink.
Bài tập: viết script MAVSDK/pymavlink cất cánh, bay hình vuông và hạ cánh.
````

## Bài 12 – Điều khiển vị trí, quỹ đạo và điều khiển nâng cao

````
BÀI 12: Điều khiển vị trí, sinh quỹ đạo và giới thiệu LQR/MPC

Mục tiêu: nâng từ điều khiển góc lên điều khiển vị trí và bám quỹ đạo.
Kiến thức cần có: Bài 9, 10; đại số tuyến tính; tối ưu cơ bản.

Nội dung bắt buộc:
- Điều khiển vị trí: vòng ngoài vị trí → vận tốc → góc/lực nâng mong muốn; phép chuyển gia tốc mong muốn thành (T, roll, pitch) và cách xử lý yaw.
- Feedforward (vận tốc/gia tốc mong muốn) để giảm sai số bám.
- Sinh quỹ đạo: nội suy đa thức, minimum snap (ý tưởng và công thức tổng quát), ràng buộc điểm qua và giới hạn động lực.
- LQR: ý tưởng chi phí, ma trận Q/R, giải Riccati (dùng thư viện), so sánh với PID.
- MPC: ý tưởng dự báo theo cửa sổ, ràng buộc, chi phí tính toán (giới thiệu, chưa đi sâu).
- Thiết kế an toàn: giới hạn góc, vận tốc, vùng bay (geofence).

Hình ảnh SVG: sơ đồ khối điều khiển vị trí; minh họa quỹ đạo qua các waypoint với/không với minimum snap.
Animation: drone bay theo quỹ đạo hình tám/vuông, hiển thị quỹ đạo mong muốn và thực tế.
Phòng thí nghiệm tương tác: kéo thả waypoint, chọn kiểu quỹ đạo, chỉnh vận tốc tối đa, xem sai số bám và gia tốc yêu cầu.
Thực hành: code Python thêm vòng vị trí và bộ sinh quỹ đạo vào mô phỏng; tùy chọn LQR bằng scipy.
Lỗi thường gặp: quỹ đạo vượt giới hạn động lực, quên feedforward gây trễ bám, windup vòng vị trí.
Bài tập: bám quỹ đạo vòng tròn bán kính 2 m; so sánh PID và LQR.
````

---

# GIAI ĐOẠN 3: PHẦN CỨNG VÀ THỰC NGHIỆM

## Bài 13 – Chọn phần cứng và kiến trúc firmware (STM32 + FreeRTOS)

````
BÀI 13: Chọn phần cứng và thiết kế kiến trúc firmware flight controller trên STM32

Mục tiêu: chọn linh kiện hợp lý và thiết kế khung firmware thời gian thực cho flight controller.
Kiến thức cần có: Bài 5, 9, 10; lập trình C, STM32, FreeRTOS.

Nội dung bắt buộc:
- Chọn linh kiện: khung, động cơ (KV, kích thước), cánh quạt, ESC, pin (cell, dung lượng, C-rate), MCU/flight controller, IMU; công thức ước lượng tỷ số lực đẩy/trọng lượng và thời gian bay.
- Sơ đồ nối dây, nguồn và bảo vệ (PDB, điện áp, nhiễu nguồn).
- Kiến trúc firmware: task điều khiển tần số cao (đồng bộ theo ngắt IMU/DMA), task cảm biến phụ, task RC input, task telemetry/log, task giám sát an toàn; độ ưu tiên, giao tiếp giữa task, đo jitter.
- Giao thức ESC: PWM, OneShot, DShot (cấu trúc khung, timer + DMA).
- Chế độ armed/disarmed, kill switch, failsafe mất tín hiệu, giám sát pin.
- Chiến lược log (blackbox) và truyền dữ liệu.

Hình ảnh SVG: sơ đồ khối phần cứng và sơ đồ task/luồng dữ liệu của firmware, kèm thời gian chu kỳ.
Animation: timeline thực thi các task theo thời gian (kiểu Gantt động) để thấy ngắt IMU kích hoạt task điều khiển.
Phòng thí nghiệm tương tác: máy tính chọn linh kiện (nhập khối lượng, động cơ, pin → tỷ số lực đẩy/trọng lượng, thời gian hover ước lượng); mô phỏng jitter và tác động lên điều khiển.
Thực hành: các bước tạo project STM32 (CubeMX), cấu hình SPI/DMA cho IMU, timer cho ESC, khung FreeRTOS với task điều khiển; code C mẫu có chú thích.
Lỗi thường gặp: ưu tiên task sai, priority inversion, nhiễu ESC ảnh hưởng IMU, quên cơ chế disarm khi lỗi.
Bài tập: tính ngân sách thời gian cho một vòng điều khiển 1 kHz.
````

## Bài 14 – Bench test từng khối: IMU, ESC/động cơ và đo thực nghiệm

````
BÀI 14: Bench test từng khối phần cứng và đo các tham số thực của động cơ

Mục tiêu: xác nhận từng khối hoạt động đúng và đo các tham số thực để đưa vào mô hình.
Kiến thức cần có: Bài 5, 13.

Nội dung bắt buộc:
- Quy trình bench test an toàn: tháo cánh quạt, kiểm tra nguồn, giới hạn dòng, cách xử lý khi có sự cố.
- Kiểm tra IMU: tần số lấy mẫu thực, độ trễ, nhiễu khi động cơ chạy (không cánh quạt, rồi có cánh quạt trên giàn đo).
- Điều khiển ESC/động cơ: hiệu chuẩn dải ga, kiểm tra chiều quay, đồng đều giữa 4 động cơ.
- Đo đường cong lực đẩy theo throttle bằng cân/loadcell; xác định k_T, k_Q, độ trễ động cơ (đáp ứng bước).
- Phân tích rung động bằng FFT từ dữ liệu IMU; nhận dạng tần số cánh quạt và cách giảm (giảm chấn, cân bằng cánh quạt, lọc).
- Cập nhật mô hình mô phỏng bằng các tham số đo được.

Hình ảnh SVG: sơ đồ giàn đo lực đẩy; hình minh họa phổ rung động.
Animation: đồ thị lực đẩy theo throttle vẽ dần khi thực hiện từng điểm đo; phổ FFT thay đổi theo tốc độ động cơ.
Phòng thí nghiệm tương tác: nhập bảng số đo (throttle, lực đẩy) để tự khớp đường cong bậc hai và hiển thị k_T; tải dữ liệu IMU (CSV) để vẽ FFT trong trình duyệt.
Thực hành: các bước từng việc, code C ghi log tốc độ cao qua UART/SD và code Python phân tích (FFT, khớp đường cong); mẫu bảng ghi kết quả đo.
Lỗi thường gặp: nguồn sụt áp khi tăng ga, nhiễu ESC trộn vào IMU, đọc sai đơn vị lực.
Bài tập: từ dữ liệu cho sẵn, tính k_T và throttle hover.
````

## Bài 15 – Giàn thử một trục và tuning PID thực tế

````
BÀI 15: Giàn thử một trục, tuning PID thực tế và an toàn

Mục tiêu: tuning PID trên drone thật một cách an toàn trước khi bay tự do.
Kiến thức cần có: Bài 6, 9, 14.

Nội dung bắt buộc:
- Thiết kế giàn thử: trục xoay một bậc tự do, dây treo, khung bảo vệ; ưu và nhược từng cách.
- Quy trình tuning thực tế: vòng trong tốc độ góc trước, rồi vòng ngoài góc; thứ tự P → D → I; dấu hiệu nhận biết từng lỗi (dao động tần số cao, rung, trôi chậm, vọt lố).
- Dùng log để tuning: đọc đồ thị setpoint, gyro, đầu ra; phân tích phổ, tìm tần số dao động.
- Cách xử lý khác biệt giữa mô phỏng và thực tế (độ trễ, bão hòa động cơ, rung).
- Kiểm tra an toàn trước khi bay: danh sách kiểm tra (checklist) trước mỗi lần bay.
- Quy tắc: kill switch luôn sẵn sàng, tháo cánh quạt khi chỉnh dây, khu vực an toàn, không bay gần người.

Hình ảnh SVG: sơ đồ giàn thử và các dạng dao động điển hình khi tuning sai.
Animation: mô phỏng giàn một trục với các hệ số PID, thấy các dạng đáp ứng tương ứng với lỗi thường gặp.
Phòng thí nghiệm tương tác: "chẩn đoán dao động": chọn một dạng đồ thị lỗi, hệ thống gợi ý hệ số cần chỉnh; checklist trước bay có thể tick.
Thực hành: các bước tuning cụ thể, code C (nhận lệnh chỉnh hệ số qua UART/telemetry để chỉnh nhanh không cần nạp lại), script Python vẽ log.
Lỗi thường gặp: tuning khi pin yếu, đổi nhiều hệ số một lúc, bỏ qua rung cơ khí.
Bài tập: cho 3 log mẫu, chẩn đoán và đề xuất thay đổi hệ số.
````

## Bài 16 – Bay thử: buộc dây, hover tự do, failsafe và phân tích log

````
BÀI 16: Quy trình bay thử, failsafe và phân tích log (blackbox)

Mục tiêu: đưa drone từ giàn thử ra bay thật và đánh giá so với mô phỏng.
Kiến thức cần có: Bài 15.

Nội dung bắt buộc:
- Các giai đoạn bay thử: bay buộc dây thấp → hover trong nhà kín với khung bảo vệ → bay ngoài trời; tiêu chí qua từng giai đoạn.
- Quy trình arm/disarm, kiểm tra trước bay, cất cánh/hạ cánh an toàn.
- Failsafe: mất tín hiệu RC, pin yếu, mất cảm biến, góc nghiêng quá lớn (crash detection); thiết kế và kiểm thử từng tình huống.
- Hover thực tế: nguyên nhân trôi, chỉnh trim, hiệu chuẩn lại.
- Phân tích log: đồ thị góc/tốc độ góc/đầu ra động cơ, nhận ra bão hòa, rung, trễ; so sánh với mô phỏng.
- Các quy định bay drone cần lưu ý (nhắc người học tự kiểm tra quy định địa phương).

Hình ảnh SVG: sơ đồ trạng thái (state machine) arm/disarm/failsafe; hình minh họa các giai đoạn bay thử.
Animation: state machine chạy động theo các sự kiện (mất tín hiệu, pin thấp) để thấy hành vi failsafe.
Phòng thí nghiệm tương tác: bảng "kịch bản sự cố" chọn tình huống → hiển thị hành vi mong đợi và cách kiểm tra; checklist bay thử.
Thực hành: code C cho state machine failsafe và cơ chế log, script Python phân tích log và so sánh mô phỏng – thực tế; mẫu báo cáo mỗi chuyến bay.
Lỗi thường gặp: failsafe không được kiểm thử, log ghi thiếu dữ liệu then chốt, bay khi chưa đạt tiêu chí giai đoạn trước.
Bài tập: thiết kế state machine cho tình huống "mất RC trong lúc bay"; viết checklist trước bay cho drone của bạn.
````

---

# GIAI ĐOẠN 4: HOÀN THIỆN VÀ MỞ RỘNG

## Bài 17 – Nhận dạng hệ thống, vòng lặp mô phỏng ↔ thực tế và mở rộng

````
BÀI 17: Nhận dạng hệ thống, vòng lặp mô phỏng ↔ thực tế và hướng mở rộng

Mục tiêu: dùng dữ liệu bay thật để cải thiện mô hình, và biết các hướng phát triển tiếp theo.
Kiến thức cần có: Bài 8–16.

Nội dung bắt buộc:
- Nhận dạng hệ thống: thiết kế tín hiệu kích thích (chirp, PRBS, bước), khớp tham số bằng bình phương tối thiểu; ước lượng quán tính, độ trễ, hằng số động cơ.
- So sánh đáp ứng thật và mô phỏng, phân tích chênh lệch và cập nhật mô hình; kiểm chứng trên dữ liệu chưa dùng để khớp.
- Đánh giá chất lượng mô hình (sai số RMS, hệ số phù hợp).
- Hướng mở rộng: optical flow + lidar/ToF giữ vị trí trong nhà, GPS và EKF vị trí, tránh vật cản, thị giác máy tính, điều khiển thích nghi.
- Gợi ý lộ trình dự án tiếp theo và cách tổ chức mã nguồn/tài liệu.

Hình ảnh SVG: vòng lặp "mô hình → mô phỏng → bay thật → log → nhận dạng → cập nhật mô hình".
Animation: đồ thị đáp ứng thật và mô phỏng dần khớp lại khi các bước nhận dạng được áp dụng.
Phòng thí nghiệm tương tác: tải dữ liệu mẫu (kích thích + đáp ứng), chọn mô hình, xem kết quả khớp và sai số thay đổi khi chỉnh tham số.
Thực hành: code Python (scipy.optimize / bình phương tối thiểu) khớp quán tính và hằng số thời gian động cơ từ log; hướng dẫn thiết kế thí nghiệm bay để thu dữ liệu tốt.
Lỗi thường gặp: kích thích không đủ phong phú, khớp quá mức (overfitting), bỏ qua nhiễu cảm biến.
Bài tập: tổng kết một báo cáo so sánh mô phỏng và thực tế cho drone của bạn.
````
