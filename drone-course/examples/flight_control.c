#include "flight_control.h"

#include <math.h>
#include <stddef.h>

static float clampf(float x, float lo, float hi) {
    return fmaxf(lo, fminf(hi, x));
}

bool flight_control_init(AttitudeController *controller, const QuadConfig *cfg,
                         const PIDController rate_pid[3]) {
    if (controller == NULL || cfg == NULL || rate_pid == NULL ||
        !isfinite(cfg->arm_xy) || !isfinite(cfg->gamma) ||
        !isfinite(cfg->k_thrust) || !isfinite(cfg->omega_max) ||
        cfg->arm_xy <= 0.0f || cfg->gamma <= 0.0f ||
        cfg->k_thrust <= 0.0f || cfg->omega_max <= 0.0f) return false;
    controller->cfg = *cfg;
    controller->mixer_saturated_last = false;
    for (int i = 0; i < 3; ++i) {
        controller->rate_pid[i] = rate_pid[i];
        controller->rate_setpoint[i] = 0.0f;
        controller->rate_pid[i].integral = 0.0f;
        controller->rate_pid[i].derivative = 0.0f;
        controller->rate_pid[i].has_previous = false;
    }
    return true;
}

void flight_control_reset(AttitudeController *controller,
                          const AttitudeEstimate *estimate) {
    if (controller == NULL || estimate == NULL) return;
    controller->mixer_saturated_last = false;
    for (int i = 0; i < 3; ++i) {
        controller->rate_setpoint[i] = 0.0f;
        pid_reset(&controller->rate_pid[i], estimate->body_rate[i]);
    }
}

bool flight_control_step(AttitudeController *controller,
                         const AttitudeEstimate *estimate,
                         const float angle_setpoint[3], float thrust_newton,
                         float dt, bool outer_due, MotorDemand *out) {
    if (controller == NULL || estimate == NULL || angle_setpoint == NULL ||
        out == NULL || !isfinite(dt) || dt <= 0.0f ||
        !isfinite(thrust_newton)) return false;
    const QuadConfig *cfg = &controller->cfg;
    for (int i = 0; i < 3; ++i) {
        if (!isfinite(estimate->euler[i]) || !isfinite(estimate->body_rate[i]) ||
            !isfinite(angle_setpoint[i])) return false;
    }
    if (outer_due) {
        for (int i = 0; i < 3; ++i) {
            float error = angle_setpoint[i] - estimate->euler[i];
            if (i == 2) error = remainderf(error, 6.28318530718f);
            controller->rate_setpoint[i] = clampf(
                cfg->angle_kp[i] * error,
                -cfg->rate_limit[i], cfg->rate_limit[i]);
        }
    }
    for (int i = 0; i < 3; ++i) {
        out->torque_cmd[i] = pid_update(&controller->rate_pid[i],
            controller->rate_setpoint[i], estimate->body_rate[i], dt,
            !controller->mixer_saturated_last);
    }
    const float tx = out->torque_cmd[0], ty = out->torque_cmd[1];
    const float tz = out->torque_cmd[2], a = cfg->arm_xy;
    const float gamma = cfg->gamma, base = thrust_newton / 4.0f;
    const float x = tx / (4.0f*a), y = ty / (4.0f*a), z = tz / (4.0f*gamma);
    const float requested[4] = {base+x-y-z, base-x-y+z,
                                base-x+y-z, base+x+y+z};
    const float max_force = cfg->k_thrust * cfg->omega_max * cfg->omega_max;
    out->mixer_saturated = false;
    for (int i = 0; i < 4; ++i) {
        const float actual = clampf(requested[i], 0.0f, max_force);
        if (fabsf(requested[i] - actual) > 1e-6f) out->mixer_saturated = true;
        out->omega_cmd[i] = sqrtf(actual / cfg->k_thrust);
    }
    controller->mixer_saturated_last = out->mixer_saturated;
    return true;
}
