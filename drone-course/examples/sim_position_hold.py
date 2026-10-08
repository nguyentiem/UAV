"""Mô phỏng cascade 12 vòng: 3 P vị trí + 3 PID vận tốc +
3 P góc + 3 PID tốc độ góc. Mô hình 6-DOF giản lược, world ENU/body FLU.

Chạy: python sim_position_hold.py
Ghi position_step.csv: bước mục tiêu x=1 m ở t=0,5 s.
"""
from __future__ import annotations

import csv
from math import atan2, cos, degrees, pi, radians, sin
from pathlib import Path

from quad_pid import PID, clamp, mixer_x, wrench_x, wrap_pi
from sim_cascade import (DT, MASS, G, J, ARM_XY, K_T, GAMMA, OMEGA_MAX,
                         MOTOR_TAU, RATE_DAMPING, quat_multiply, euler_from_quat)


def body_z_in_world(q):
    """Cột 3 của R(q), q=[w,x,y,z] đổi body -> world."""
    w, x, y, z = q
    return (2*(x*z + w*y), 2*(y*z - w*x), 1 - 2*(x*x + y*y))


def main(output: Path | None = None):
    output = output or Path(__file__).with_name("position_step.csv")
    pos = [0.0, 0.0, 1.0]
    vel = [0.0, 0.0, 0.0]
    q = (1.0, 0.0, 0.0, 0.0)
    rate = [0.0, 0.0, 0.0]
    omega_hover = (MASS * G / (4 * K_T)) ** 0.5
    omega = [omega_hover] * 4
    pos_kp = (1.2, 1.2, 1.2)      # 1/s
    vel_sp_limit = (1.5, 1.5, 1.0)  # m/s
    vel_pid = [PID(2.0, .35, .06, 3.0, .8, 15.0),
               PID(2.0, .35, .06, 3.0, .8, 15.0),
               PID(2.5, .6, .08, 3.0, 1.0, 15.0)]
    for axis in range(3):
        vel_pid[axis].reset(vel[axis])
    angle_kp = (4.0, 4.0, 2.0)
    rate_limit = (2.0, 2.0, 1.5)
    rate_pid = [PID(.07, .025, .001, .25, .10),
                PID(.07, .025, .001, .25, .10),
                PID(.09, .025, .001, .12, .05)]
    for axis in range(3):
        rate_pid[axis].reset(rate[axis])
    velocity_sp = [0.0, 0.0, 0.0]
    acceleration_sp = [0.0, 0.0, 0.0]
    angle_sp = [0.0, 0.0, 0.0]
    rate_sp = [0.0, 0.0, 0.0]
    thrust_cmd = MASS * G
    mixer_saturated = False
    rows = []
    for k in range(int(8.0 / DT)):
        t = k * DT
        position_sp = (1.0 if t >= .5 else 0.0, 0.0, 1.0)
        if k % 10 == 0:  # 50 Hz: vòng vị trí P -> vận tốc mục tiêu
            for i in range(3):
                velocity_sp[i] = clamp(pos_kp[i] * (position_sp[i] - pos[i]),
                                       -vel_sp_limit[i], vel_sp_limit[i])
        if k % 5 == 0:  # 100 Hz: PID vận tốc -> gia tốc mục tiêu
            for i in range(3):
                acceleration_sp[i] = vel_pid[i].update(
                    velocity_sp[i], vel[i], 5*DT,
                    allow_integral=not mixer_saturated)
            ax, ay, az = acceleration_sp
            # Yaw mục tiêu = 0; với góc nhỏ ax≈g*theta, ay≈-g*phi.
            up = max(1.0, G + az)
            angle_sp[0] = clamp(-atan2(ay, up), -radians(25), radians(25))
            angle_sp[1] = clamp(atan2(ax, up), -radians(25), radians(25))
            angle_sp[2] = 0.0
            thrust_cmd = MASS * up / (cos(angle_sp[0]) * cos(angle_sp[1]))
            # 100 Hz: vòng góc P -> tốc độ góc mục tiêu
            angle = euler_from_quat(q)
            for i in range(3):
                error = wrap_pi(angle_sp[i] - angle[i]) if i == 2 else angle_sp[i] - angle[i]
                rate_sp[i] = clamp(angle_kp[i] * error,
                                   -rate_limit[i], rate_limit[i])
        # 500 Hz: PID tốc độ góc -> mixer -> motor.
        torque_cmd = tuple(rate_pid[i].update(rate_sp[i], rate[i], DT,
                           allow_integral=not mixer_saturated) for i in range(3))
        omega_cmd, mixer_saturated = mixer_x(thrust_cmd, torque_cmd,
                                              ARM_XY, GAMMA, K_T, OMEGA_MAX)
        for i in range(4):
            omega[i] += DT * (omega_cmd[i] - omega[i]) / MOTOR_TAU
        thrust, torque = wrench_x(omega, ARM_XY, GAMMA, K_T)
        body_z = body_z_in_world(q)
        # Cản tuyến tính chỉ để chuyển động tịnh tiến tắt dần trong mô phỏng.
        for i in range(3):
            gravity = -G if i == 2 else 0.0
            acceleration = gravity + thrust * body_z[i] / MASS - .12 * vel[i]
            vel[i] += DT * acceleration
            pos[i] += DT * vel[i]
        jw = [J[i] * rate[i] for i in range(3)]
        cross = (rate[1]*jw[2] - rate[2]*jw[1],
                 rate[2]*jw[0] - rate[0]*jw[2],
                 rate[0]*jw[1] - rate[1]*jw[0])
        for i in range(3):
            rate[i] += DT * (torque[i] - cross[i] - RATE_DAMPING[i]*rate[i]) / J[i]
        dq = quat_multiply(q, (0.0, *rate))
        q = tuple(q[i] + .5*DT*dq[i] for i in range(4))
        norm = sum(value*value for value in q) ** .5
        q = tuple(value/norm for value in q)
        angle = euler_from_quat(q)
        rows.append((t, position_sp[0], *pos, *vel,
                     degrees(angle[0]), degrees(angle[1]), thrust,
                     *omega, int(mixer_saturated)))
    with output.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(("time_s", "x_sp_m", "x_m", "y_m", "z_m",
                         "vx_m_s", "vy_m_s", "vz_m_s", "roll_deg", "pitch_deg",
                         "thrust_N", "omega1", "omega2", "omega3", "omega4",
                         "saturated"))
        writer.writerows(rows)
    print(f"CSV: {output}\nFinal x={pos[0]:.3f} m, y={pos[1]:.3f} m, z={pos[2]:.3f} m")
    print(f"Mixer saturation samples: {sum(row[-1] for row in rows)} / {len(rows)}")
    return rows


if __name__ == "__main__":
    main()
