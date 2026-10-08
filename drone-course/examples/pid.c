#include "pid.h"

#include <math.h>
#include <stddef.h>

static float clampf(float x, float lo, float hi) {
    return fmaxf(lo, fminf(hi, x));
}

void pid_reset(PIDController *pid, float measurement) {
    if (pid == NULL) return;
    pid->integral = 0.0f;
    pid->derivative = 0.0f;
    pid->previous_measurement = measurement;
    pid->has_previous = true;
}

float pid_update(PIDController *pid, float setpoint, float measurement,
                 float dt, bool allow_integral) {
    if (pid == NULL || !isfinite(setpoint) || !isfinite(measurement) ||
        !isfinite(dt) || dt <= 0.0f || pid->output_limit <= 0.0f ||
        pid->integral_limit < 0.0f) return 0.0f;
    const float error = setpoint - measurement;
    if (!pid->has_previous) pid_reset(pid, measurement);
    const float raw_d = -(measurement - pid->previous_measurement) / dt;
    pid->previous_measurement = measurement;
    if (pid->d_cutoff_hz > 0.0f) {
        const float alpha = 1.0f - expf(-6.28318530718f * pid->d_cutoff_hz * dt);
        pid->derivative += alpha * (raw_d - pid->derivative);
    } else {
        pid->derivative = 0.0f;
    }
    const float p = pid->kp * error;
    const float d = pid->kd * pid->derivative;
    float candidate_i = pid->integral;
    if (allow_integral) {
        candidate_i = clampf(pid->integral + pid->ki * error * dt,
                             -pid->integral_limit, pid->integral_limit);
    }
    const float tentative = p + candidate_i + d;
    const bool pushes_upper = tentative > pid->output_limit && error > 0.0f;
    const bool pushes_lower = tentative < -pid->output_limit && error < 0.0f;
    if (allow_integral && !pushes_upper && !pushes_lower) pid->integral = candidate_i;
    return clampf(p + pid->integral + d, -pid->output_limit, pid->output_limit);
}
