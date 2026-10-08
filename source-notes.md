  
  

CƠ SỞ LÝ THUYẾT ĐỂ XÂY DỰNG QUADCOPTER

**Từ vật lý - toán học đến cảm biến, điều khiển và flight controller**

  
Tài liệu nhập môn dành cho người mới

  

# 1. Bức tranh tổng thể: quadcopter thực sự đang làm gì?

Một quadcopter có bốn động cơ/cánh quạt. Bốn động cơ tạo ra lực nâng và mô-men, từ đó làm thay đổi chuyển động tịnh tiến và chuyển động quay của thân drone.

FRONT  
↑  
M1 ↻ ↺ M2  
\\ /  
\\ /  
[O]  
/ \\  
/ \\  
M4 ↺ ↻ M3

Drone là một vật rắn có 6 bậc tự do (6-DOF):

- Tịnh tiến theo X, Y, Z.
- Quay Roll (φ), Pitch (θ), Yaw (ψ).

Tuy nhiên quadcopter chỉ có bốn cơ cấu chấp hành chính: tốc độ của bốn motor. Bài toán điều khiển cốt lõi là biến bốn tốc độ motor thành tổng lực và ba mô-men.

*[ω1, ω2, ω3, ω4] → [F, τx, τy, τz] → chuyển động*

# 2. Nền tảng vật lý số 1: Định luật II Newton

*ΣF = m a*

Motor không trực tiếp điều khiển vị trí. Motor tạo lực; lực tạo gia tốc; gia tốc làm thay đổi vận tốc; vận tốc làm thay đổi vị trí.

*a = dv/dt*

*v = dx/dt*

*d²x/dt² = F/m*

Chuỗi nhân quả này là nền móng để hiểu flight controller: controller tác động vào lực/mô-men, sau đó động lực học của drone quyết định trạng thái chuyển động.

# 3. Vì sao drone bay lên?

↑ T  
│  
┌─────┐  
│Drone│  
└─────┘  
│  
↓ mg

Trọng lực có độ lớn:

*Fg = m g*

Tổng thrust của bốn motor:

*T = T1 + T2 + T3 + T4*

Theo Newton theo phương thẳng đứng, trong mô hình đơn giản:

*m z¨ = T - mg*

*z¨ = T/m - g*

## 3.1. Điều kiện hover

Khi drone đứng yên ở độ cao không đổi, gia tốc thẳng đứng bằng 0:

*T = mg*

Ví dụ drone 1 kg cần tổng thrust xấp xỉ 9,81 N để hover. Nếu bốn motor chia đều tải, mỗi motor cần khoảng 2,45 N trong điều kiện lý tưởng.

# 4. Mô hình motor và cánh quạt

Mô hình cơ bản thường dùng cho thrust của một rotor:

*Ti = kf ωi²*

Reaction torque của rotor có thể được mô hình hóa:

*Qi = km ωi²*

- ωi: tốc độ góc của rotor.
- kf: hệ số thrust, phụ thuộc cánh quạt, mật độ không khí, hình học và điều kiện làm việc.
- km: hệ số mô-men phản lực.

Vì thrust gần tỷ lệ với bình phương tốc độ rotor trong mô hình lý tưởng, quan hệ PWM → RPM → thrust không phải một quan hệ tuyến tính đơn giản.

# 5. Mô-men lực và chuyển động quay

*τ = r × F*

Trong trường hợp lực vuông góc với cánh tay đòn:

*τ = r F*

↑ F  
│  
●───────────●  
CG r Motor

Lực của motor đặt cách tâm khối lượng tạo mô-men quanh tâm. Đây là cơ sở để quadcopter điều khiển Roll và Pitch.

# 6. Roll và Pitch

## 6.1. Roll

Left Right  
↑ TL ↑ TR  
\\ /  
\\\_\_\_\_\_\_\_\_\_\_\_/  
CG

Nếu thrust bên phải lớn hơn bên trái, xuất hiện mô-men quanh trục Roll. Drone bắt đầu có gia tốc góc và nghiêng sang một phía.

## 6.2. Pitch

Pitch hoạt động tương tự nhưng sử dụng chênh lệch thrust giữa nhóm motor phía trước và phía sau.

Điểm quan trọng: quadcopter không cần một động cơ riêng đẩy ngang. Muốn tiến về phía trước, nó nghiêng thân để nghiêng vector tổng thrust.

# 7. Phân tích vector thrust

Khi drone nghiêng một góc θ, tổng thrust có thể phân tích thành các thành phần:

*Tz = T cos(θ)*

*Tx = T sin(θ)*

Tx tạo gia tốc ngang, còn Tz chống lại trọng lực. Vì cos(θ) &lt; 1 khi drone nghiêng, nếu giữ nguyên tổng thrust thì thành phần thẳng đứng giảm và drone có xu hướng tụt độ cao.

Muốn giữ độ cao trong mô hình đơn giản:

*T cos(θ) = mg*

*T = mg / cos(θ)*

Ví dụ ở 30°, 1/cos(30°) ≈ 1,155, tức tổng thrust cần tăng khoảng 15,5% so với hover lý tưởng.

# 8. Yaw và phản lực mô-men

Yaw khác Roll/Pitch. Khi motor làm quay propeller, propeller tác dụng mô-men ngược lại lên thân drone. Để các mô-men này triệt tiêu khi hover, các rotor được bố trí quay xen kẽ CW và CCW.

M1 CW M2 CCW  
  
M4 CCW M3 CW

Muốn tạo yaw, controller thay đổi tương đối tốc độ của hai nhóm CW/CCW, đồng thời cố giữ tổng thrust theo yêu cầu.

# 9. Động lực học quay và moment quán tính

Phiên bản đơn giản của định luật Newton cho chuyển động quay quanh một trục:

*τ = I α*

*α = dω/dt*

*ω = dθ/dt*

*τ = I d²θ/dt²*

I là moment quán tính. Khối lượng càng phân bố xa trục quay thì I càng lớn. Với cùng mô-men τ, vật có I lớn sẽ có gia tốc góc α nhỏ hơn.

Do đó hai drone cùng khối lượng nhưng khác chiều dài tay đòn hoặc phân bố pin/motor có thể có đáp ứng điều khiển rất khác nhau.

# 10. Hệ tọa độ Body và World

Các cảm biến và phương trình điều khiển cần phân biệt hệ tọa độ gắn với drone (body frame) và hệ tọa độ cố định theo môi trường/navigation frame (world frame).

- Body frame quay cùng drone; IMU thường trả dữ liệu trong hệ này.
- World/navigation frame dùng để mô tả vị trí, vận tốc và hướng so với môi trường.

Nếu vector thrust trong body frame là:

*Tb = [0, 0, T]ᵀ*

thì chuyển sang world frame bằng ma trận quay R:

*Tw = R Tb*

Mô hình tịnh tiến 3D có dạng khái quát:

*m p¨ = Tw + Fg + các lực khác*

# 11. Euler angles và Rotation Matrix

Một biểu diễn trực quan của orientation là:

*φ = Roll, θ = Pitch, ψ = Yaw*

Một quy ước thường gặp xây ma trận quay:

*R = Rz(ψ) Ry(θ) Rx(φ)*

Ví dụ ma trận quay quanh trục X:

*Rx(φ) = [[1,0,0],[0,cosφ,-sinφ],[0,sinφ,cosφ]]*

Euler angles dễ hiểu nhưng có singularity/gimbal lock với một số cấu hình góc. Vì vậy flight controller thường dùng quaternion hoặc rotation matrix ở bên trong.

# 12. Quaternion

*q = [w, x, y, z]*

*w² + x² + y² + z² = 1*

Quaternion là cách biểu diễn orientation 3D gọn, tránh singularity kiểu Euler trong biểu diễn orientation và rất phù hợp cho tích phân gyro, sensor fusion và phép quay vector.

Gyroscope ─┐  
│  
Accel ─────┼──&gt; Sensor Fusion ──&gt; Quaternion  
│  
Mag ───────┘

# 13. Cảm biến: drone biết mình đang nghiêng thế nào?

## 13.1. Gyroscope

Gyroscope đo tốc độ góc ωx, ωy, ωz. Góc có thể được cập nhật bằng tích phân:

*θ(t) = θ(0) + ∫ω(t) dt*

Nhược điểm là bias và noise được tích lũy theo thời gian, gây drift.

## 13.2. Accelerometer

Accelerometer đo specific force. Khi drone gần tĩnh hoặc gia tốc tịnh tiến nhỏ, hướng trọng lực biểu kiến có thể được dùng làm tham chiếu để ước lượng Roll/Pitch.

*φ ≈ atan2(ay, az)*

Accelerometer không chịu drift tích phân như gyro, nhưng bị ảnh hưởng bởi rung motor và gia tốc chuyển động.

# 14. Sensor Fusion

Gyro tốt ở biến đổi nhanh/ngắn hạn nhưng drift dài hạn; accelerometer có tham chiếu trọng lực tốt hơn ở tần số thấp nhưng nhiễu khi drone tăng tốc. Sensor fusion kết hợp ưu điểm của cả hai.

## 14.1. Complementary Filter

*θ = α(θold + ωΔt) + (1-α) θacc*

Ví dụ α = 0,98: thành phần gyro chi phối đáp ứng ngắn hạn, còn accelerometer từ từ hiệu chỉnh drift.

Các bước nâng cao tiếp theo gồm Mahony, Madgwick, Kalman Filter và EKF.

# 15. Từ State Estimation đến Control

Controller nhận trạng thái mong muốn và trạng thái ước lượng. Ví dụ Roll mục tiêu 10°, Roll hiện tại 7°:

*e = 10° - 7° = 3°*

Từ sai số này, controller tính yêu cầu mô-men hoặc angular-rate để đưa drone về trạng thái mong muốn.

# 16. PID

*u(t) = Kp e(t) + Ki ∫e(t)dt + Kd de(t)/dt*

- P: phản ứng theo sai số hiện tại.
- I: tích lũy sai số kéo dài và giúp loại bỏ sai lệch tĩnh.
- D: phản ứng theo tốc độ thay đổi của sai số, tạo damping nhưng nhạy với noise.

Trong flight controller thực tế, PID thường làm việc trong cấu trúc nhiều vòng chứ không chỉ một PID từ góc trực tiếp ra motor.

# 17. Cascade Control

Position target  
↓  
Position Controller  
↓  
Velocity target  
↓  
Velocity Controller  
↓  
Attitude target  
↓  
Attitude Controller  
↓  
Angular-rate target  
↓  
Rate Controller  
↓  
Torque / Thrust  
↓  
Mixer  
↓  
Motors

Vòng trong, đặc biệt angular-rate loop, thường chạy nhanh hơn các vòng ngoài. Cấu trúc cascade giúp tách các bài toán điều khiển theo thang thời gian.

# 18. Mixer / Control Allocation

Controller có thể tạo vector yêu cầu:

*u = [T, τx, τy, τz]ᵀ*

Bốn rotor tạo vector thrust:

*f = [T1, T2, T3, T4]ᵀ*

Quan hệ lý tưởng có thể viết:

*u = A f*

Nếu A khả nghịch trong cấu hình đang xét:

*f = A⁻¹ u*

Ma trận A phụ thuộc hình học frame, vị trí rotor, chiều quay và hệ số thrust/torque. Trong hệ thống thực tế còn phải xử lý saturation, giới hạn motor và ưu tiên các trục điều khiển.

# 19. Closed-loop flight control hoàn chỉnh

Pilot / Navigation  
↓  
Desired State  
↓  
Controller  
↓  
Thrust + Torque  
↓  
Mixer  
↓  
ESC / Motors  
↓  
Force + Torque  
↓  
Drone Dynamics  
↓  
Actual State  
↓  
IMU / Barometer / GPS / Magnetometer  
↓  
State Estimator  
└──────────────────→ Controller

Đây là vòng kín: cảm biến quan sát kết quả của tác động điều khiển, estimator ước lượng trạng thái, controller tính tác động mới và quá trình lặp lại liên tục.

# 20. Những phần toán cần học

|                            |                                    |
| -------------------------- | ---------------------------------- |
| Chủ đề toán học            | Ứng dụng trong quadcopter          |
| Đại số                     | Phương trình và biến đổi công thức |
| Lượng giác                 | Phân tích vector thrust và góc     |
| Vector                     | Lực, vận tốc, gia tốc              |
| Tích vô hướng              | Góc giữa các vector                |
| Tích có hướng              | Mô-men lực                         |
| Ma trận                    | Biến đổi hệ tọa độ                 |
| Đạo hàm                    | Vận tốc, gia tốc, tốc độ góc       |
| Tích phân                  | Vị trí, góc, tích lũy sai số       |
| ODE                        | Mô hình động lực học               |
| Quaternion                 | Orientation 3D                     |
| Đại số tuyến tính          | State-space, estimator, EKF        |
| Xác suất &amp; thống kê    | Noise, covariance, estimation      |
| Laplace / frequency domain | Phân tích control và stability     |

# 21. Lộ trình học đề xuất

**Phần I - Vật lý cơ bản:** Vector, Newton, trọng lực, thrust, mô-men, moment quán tính, chuyển động tịnh tiến và quay.

**Phần II - Toán 3D:** Hệ tọa độ, rotation matrix, Euler angles, quaternion.

**Phần III - Mô hình quadcopter:** Motor/propeller, thrust, torque, rigid-body 6-DOF, mixer/control allocation.

**Phần IV - Cảm biến:** Accelerometer, gyroscope, magnetometer, barometer, GPS; bias, noise, drift, calibration.

**Phần V - State Estimation:** Complementary filter, Mahony/Madgwick, Kalman Filter, EKF.

**Phần VI - Control Theory:** Feedback, stability, PID, rate/attitude/altitude/position control, cascade control.

**Phần VII - Flight Controller thực tế:** Sampling, discrete-time control, filtering, ESC/DShot, scheduler/RTOS, failsafe, watchdog, logging.

**Phần VIII - Tự xây drone:** Chọn motor/prop/ESC/battery, tính thrust-to-weight, IMU, estimator, PID, mixer, test và tuning.

# 22. Tư duy xuyên suốt

Không nên bắt đầu bằng việc thuộc công thức PID. Hãy luôn bám theo chuỗi vật lý và thông tin:

*Motor → Force/Torque → Dynamics → Sensor → Estimation → Control → Motor*

Khi hiểu được chuỗi này, PID, EKF, quaternion hay mixer không còn là các khối rời rạc. Mỗi khối giải quyết một vấn đề cụ thể trong vòng điều khiển.

# 23. Bước học tiếp theo

Bài tiếp theo nên bắt đầu từ Vector - lực - mô-men - hệ tọa độ, sau đó tự suy ra từng bước phương trình động lực học 6-DOF của quadcopter. Sau khi mô hình vật lý rõ ràng mới chuyển sang cảm biến, estimator và controller.
