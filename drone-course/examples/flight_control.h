#ifndef DRONE_FLIGHT_CONTROL_H
#define DRONE_FLIGHT_CONTROL_H

#include "pid.h"

typedef struct {
    float arm_xy;       /* L / sqrt(2), m */
    float gamma;        /* kQ / kT, m */
    float k_thrust;     /* N / (rad/s)^2 */
    float omega_max;    /* rad/s */
    float angle_kp[3];  /* 1/s: roll, pitch, yaw */
    float rate_limit[3];/* rad/s */
} QuadConfig;

typedef struct {
    QuadConfig cfg;
    PIDController rate_pid[3];
    float rate_setpoint[3];
    bool mixer_saturated_last;
} AttitudeController;

typedef struct {
    float euler[3];       /* rad: roll, pitch, yaw from estimator */
    float body_rate[3];   /* rad/s: gyro after calibration/filtering */
} AttitudeEstimate;

typedef struct {
    float omega_cmd[4];  /* rad/s, motor 1..4 */
    float torque_cmd[3]; /* N*m */
    bool mixer_saturated;
} MotorDemand;

bool flight_control_init(AttitudeController *controller, const QuadConfig *cfg,
                         const PIDController rate_pid[3]);
void flight_control_reset(AttitudeController *controller,
                          const AttitudeEstimate *estimate);
bool flight_control_step(AttitudeController *controller,
                         const AttitudeEstimate *estimate,
                         const float angle_setpoint[3], float thrust_newton,
                         float dt, bool outer_due, MotorDemand *out);

#endif
