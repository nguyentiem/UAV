"""Mô phỏng 3 trục quay, 4 motor, P góc ngoài + PID tốc độ góc trong.

Chạy: python sim_cascade.py
Kết quả: attitude_step.csv và các chỉ số ngắn trên terminal.
Không mô phỏng vị trí, cảm biến, pin hay khí động học bay tiến.
"""
from __future__ import annotations

import csv
from math import asin, atan2, cos, degrees, pi, radians, sin
from pathlib import Path

from quad_pid import PID, clamp, mixer_x, wrap_pi, wrench_x

DT = 0.002             # 500 Hz: vòng rate, động học và motor
OUTER_DIV = 5          # 100 Hz: vòng góc
MASS = 1.0             # kg
G = 9.81               # m/s²
J = (0.020, 0.020, 0.040)  # kg·m²: roll, pitch, yaw
ARM_XY = 0.18          # m = L/sqrt(2)
K_T = 1.5e-5           # N/(rad/s)²
GAMMA = 0.020          # m = kQ/kT
OMEGA_MAX = 650.0      # rad/s
MOTOR_TAU = 0.025      # s
RATE_DAMPING = (0.006, 0.006, 0.010)  # N·m·s/rad, minh họa


def quat_multiply(a, b):
    aw, ax, ay, az = a
    bw, bx, by, bz = b
    return (aw*bw - ax*bx - ay*by - az*bz,
            aw*bx + ax*bw + ay*bz - az*by,
            aw*by - ax*bz + ay*bw + az*bx,
            aw*bz + ax*by - ay*bx + az*bw)


def euler_from_quat(q):
    w, x, y, z = q
    roll = atan2(2*(w*x + y*z), 1 - 2*(x*x + y*y))
    pitch = asin(clamp(2*(w*y - z*x), -1.0, 1.0))
    yaw = atan2(2*(w*z + x*y), 1 - 2*(y*y + z*z))
    return roll, pitch, yaw


def main(output: Path | None = None):
    output = output or Path(__file__).with_name("attitude_step.csv")
    q = (1.0, 0.0, 0.0, 0.0)  # body -> world
    rate = [0.0, 0.0, 0.0]
    omega_hover = (MASS * G / (4 * K_T)) ** 0.5
    omega = [omega_hover] * 4
    angle_kp = (4.0, 4.0, 2.0)   # 1/s
    rate_limit = (2.0, 2.0, 1.5)  # rad/s
    rate_pid = [PID(0.07, 0.025, 0.001, 0.25, 0.10),
                PID(0.07, 0.025, 0.001, 0.25, 0.10),
                PID(0.09, 0.025, 0.001, 0.12, 0.05)]
    for axis in range(3):
        rate_pid[axis].reset(rate[axis])
    rate_sp = [0.0, 0.0, 0.0]
    mixer_saturated = False
    rows = []
    for k in range(int(5.0 / DT)):
        time = k * DT
        # Mục tiêu roll +10° từ 0,5 đến 2,5 s, sau đó trở về 0°.
        angle_sp = (radians(10.0) if 0.5 <= time < 2.5 else 0.0, 0.0, 0.0)
        angle = euler_from_quat(q)
        if k % OUTER_DIV == 0:
            for axis in range(3):
                error = (wrap_pi(angle_sp[axis] - angle[axis]) if axis == 2
                         else angle_sp[axis] - angle[axis])
                rate_sp[axis] = clamp(angle_kp[axis] * error,
                                      -rate_limit[axis], rate_limit[axis])
        torque_cmd = tuple(rate_pid[i].update(rate_sp[i], rate[i], DT,
                            allow_integral=not mixer_saturated) for i in range(3))
        omega_cmd, mixer_saturated = mixer_x(MASS*G, torque_cmd, ARM_XY,
                                              GAMMA, K_T, OMEGA_MAX)
        for i in range(4):
            omega[i] += DT * (omega_cmd[i] - omega[i]) / MOTOR_TAU
        thrust, torque = wrench_x(omega, ARM_XY, GAMMA, K_T)
        jw = [J[i] * rate[i] for i in range(3)]
        cross = (rate[1]*jw[2] - rate[2]*jw[1],
                 rate[2]*jw[0] - rate[0]*jw[2],
                 rate[0]*jw[1] - rate[1]*jw[0])
        for i in range(3):
            rate[i] += DT * (torque[i] - cross[i] - RATE_DAMPING[i]*rate[i]) / J[i]
        dq = quat_multiply(q, (0.0, *rate))
        q = tuple(q[i] + 0.5*DT*dq[i] for i in range(4))
        norm = sum(value*value for value in q) ** 0.5
        q = tuple(value/norm for value in q)
        rows.append((time, degrees(angle_sp[0]), degrees(angle[0]),
                     degrees(rate[0]), thrust, *omega, int(mixer_saturated)))
    with output.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(("time_s", "roll_sp_deg", "roll_deg", "roll_rate_deg_s",
                         "thrust_N", "omega1", "omega2", "omega3", "omega4", "saturated"))
        writer.writerows(rows)
    peak = max(row[2] for row in rows if 0.5 <= row[0] < 2.5)
    held = next(row[2] for row in rows if row[0] >= 2.4)
    final = rows[-1][2]
    print(f"CSV: {output}\nRoll at 2.4 s: {held:.2f} deg; peak: {peak:.2f} deg; final: {final:.2f} deg")
    print(f"Mixer saturation samples: {sum(row[-1] for row in rows)} / {len(rows)}")
    return rows


if __name__ == "__main__":
    main()
