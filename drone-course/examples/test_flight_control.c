#include "flight_control.h"

#include <assert.h>
#include <math.h>
#include <stdio.h>

int main(void) {
    QuadConfig cfg = {.arm_xy = 0.18f, .gamma = 0.02f,
        .k_thrust = 1.5e-5f, .omega_max = 650.0f,
        .angle_kp = {4.0f,4.0f,2.0f}, .rate_limit = {2.0f,2.0f,1.5f}};
    PIDController pids[3] = {
        {.kp=.07f,.ki=.025f,.kd=.001f,.output_limit=.25f,.integral_limit=.10f,.d_cutoff_hz=30.0f},
        {.kp=.07f,.ki=.025f,.kd=.001f,.output_limit=.25f,.integral_limit=.10f,.d_cutoff_hz=30.0f},
        {.kp=.09f,.ki=.025f,.kd=.001f,.output_limit=.12f,.integral_limit=.05f,.d_cutoff_hz=30.0f}};
    AttitudeController controller;
    assert(flight_control_init(&controller, &cfg, pids));
    const AttitudeEstimate level = {{0,0,0},{0,0,0}};
    const float level_sp[3] = {0,0,0};
    MotorDemand out;
    assert(flight_control_step(&controller, &level, level_sp, 9.81f,
                               .002f, true, &out));
    assert(!out.mixer_saturated);
    for (int i=1; i<4; ++i) assert(fabsf(out.omega_cmd[i]-out.omega_cmd[0]) < .001f);
    const float roll_sp[3] = {.174532925f,0,0};
    assert(flight_control_step(&controller, &level, roll_sp, 9.81f,
                               .002f, true, &out));
    assert(out.omega_cmd[0] > out.omega_cmd[1]);
    assert(out.omega_cmd[3] > out.omega_cmd[2]);
    printf("C controller: hover and positive roll allocation OK\n");
    return 0;
}
