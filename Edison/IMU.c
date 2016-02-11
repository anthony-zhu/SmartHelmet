#include <stdio.h>
#include <math.h>
#include <mraa/i2c.h>
#include "LSM9DS0.h"
int main() {
    setvbuf(stdout, (char *) NULL, _IOLBF, 0); /* make line buffered stdout */

    mraa_i2c_context accel, gyro, mag;
    float a_res, g_res, m_res;
    data_t accel_data, gyro_data, mag_data;
    int16_t temperature;

    accel = accel_init();
    set_accel_scale(accel, A_SCALE_16G);
    set_accel_ODR(accel, A_ODR_100);
    a_res = calc_accel_res(A_SCALE_16G);

    while(1) {
        accel_data = read_accel(accel, a_res);

        printf("{\"accel\":{\"x\":%.5f,\"y\":%.5f,\"z\":%.5f}}\n", accel_data.x,
                accel_data.y, accel_data.z);

        // Sleep for 10000 microseconds (0.01 seconds)
        usleep(10000);
    }

    return 0;
}
