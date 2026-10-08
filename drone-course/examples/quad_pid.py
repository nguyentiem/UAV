"""Bộ PID rời rạc minh họa. Quy ước ENU/FLU, góc/rate dùng rad và rad/s."""
from dataclasses import dataclass
from math import exp, isfinite, pi


def clamp(value: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, value))


def wrap_pi(angle: float) -> float:
    return (angle + pi) % (2 * pi) - pi


@dataclass
class PID:
    kp: float
    ki: float
    kd: float
    output_limit: float
    integral_limit: float
    d_cutoff_hz: float = 30.0
    integral: float = 0.0
    derivative: float = 0.0
    previous_measurement: float | None = None

    def reset(self, measurement: float = 0.0) -> None:
        self.integral = 0.0
        self.derivative = 0.0
        self.previous_measurement = measurement

    def update(
        self,
        setpoint: float,
        measurement: float,
        dt: float,
        *,
        allow_integral: bool = True,
    ) -> float:
        if not all(map(isfinite, (setpoint, measurement, dt))) or dt <= 0.0:
            raise ValueError("setpoint, measurement và dt phải hữu hạn; dt > 0")
        error = setpoint - measurement
        if self.previous_measurement is None:
            self.previous_measurement = measurement
        raw_d = -(measurement - self.previous_measurement) / dt
        self.previous_measurement = measurement
        # Lọc thông thấp trên đạo hàm của phép đo, tránh derivative kick khi đổi setpoint.
        if self.d_cutoff_hz > 0.0:
            alpha = 1.0 - exp(-2.0 * pi * self.d_cutoff_hz * dt)
            self.derivative += alpha * (raw_d - self.derivative)
        else:
            self.derivative = 0.0
        p_term = self.kp * error
        d_term = self.kd * self.derivative
        candidate_i = self.integral
        if allow_integral:
            candidate_i = clamp(
                self.integral + self.ki * error * dt,
                -self.integral_limit,
                self.integral_limit,
            )
        tentative = p_term + candidate_i + d_term
        # Nếu đang chạm giới hạn và sai số đẩy sâu hơn vào giới hạn, không tích phân.
        pushes_upper = tentative > self.output_limit and error > 0.0
        pushes_lower = tentative < -self.output_limit and error < 0.0
        if allow_integral and not (pushes_upper or pushes_lower):
            self.integral = candidate_i
        return clamp(p_term + self.integral + d_term, -self.output_limit, self.output_limit)


def mixer_x(thrust: float, torque: tuple[float, float, float], arm_xy: float,
            gamma: float, k_thrust: float, omega_max: float) -> tuple[list[float], bool]:
    """Trả Ω_cmd[1..4] rad/s và cờ bão hòa. M1/M3 CCW, M2/M4 CW."""
    if min(arm_xy, gamma, k_thrust, omega_max) <= 0.0:
        raise ValueError("Hình học và hằng số motor phải dương")
    tx, ty, tz = torque
    base = thrust / 4.0
    x, y, z = tx / (4 * arm_xy), ty / (4 * arm_xy), tz / (4 * gamma)
    requested = [base + x - y - z, base - x - y + z,
                 base - x + y - z, base + x + y + z]
    max_force = k_thrust * omega_max**2
    limited = [clamp(force, 0.0, max_force) for force in requested]
    saturated = any(abs(a - b) > 1e-10 for a, b in zip(requested, limited))
    return [(force / k_thrust) ** 0.5 for force in limited], saturated


def wrench_x(omega: list[float], arm_xy: float, gamma: float,
             k_thrust: float) -> tuple[float, tuple[float, float, float]]:
    f1, f2, f3, f4 = [k_thrust * value**2 for value in omega]
    return (f1 + f2 + f3 + f4,
            (arm_xy * (f1 - f2 - f3 + f4),
             arm_xy * (-f1 - f2 + f3 + f4),
             gamma * (-f1 + f2 - f3 + f4)))
