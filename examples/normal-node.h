#ifndef NORMAL_NODE_H
#define NORMAL_NODE_H

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdlib.h>
#include <signal.h>
#include <string.h>
#include <ctype.h>
#include <time.h>
#include <pthread.h>
#include <stdbool.h>
#include <setjmp.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

void on_data(const uint8_t* rawdata, uint32_t data_size, ndn_face_intf_t* face);

#ifdef __cplusplus
}
#endif

#endif