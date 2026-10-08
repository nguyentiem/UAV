#ifndef DRONE_PID_H
#define DRONE_PID_H

#include <stdbool.h>

typedef struct {
    float kp, ki, kd;
    float output_limit, integral_limit, d_cutoff_hz;
    float integral, derivative, previous_measurement;
    bool has_previous;
} PIDController;

void pid_reset(PIDController *pid, float measurement);
float pid_update(PIDController *pid, float setpoint, float measurement,
                 float dt, bool allow_integral);

#endif
