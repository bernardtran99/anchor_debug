#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>
#include <string.h>
#include <ctype.h>
#include <time.h>
#include <pthread.h>
#include <stdbool.h>
#include <setjmp.h>
#include <netdb.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <netinet/tcp.h> 
#include <ndn-lite.h>
#include "ndn-lite.h"
#include "ndn-lite/encode/name.h"
#include "ndn-lite/encode/data.h"
#include "ndn-lite/encode/interest.h"
#include "ndn-lite/encode/signed-interest.h"
#include "ndn-lite/app-support/service-discovery.h"
#include "ndn-lite/app-support/access-control.h"
#include "ndn-lite/app-support/security-bootstrapping.h"
#include "ndn-lite/app-support/ndn-sig-verifier.h"
#include "ndn-lite/app-support/pub-sub.h"
#include "ndn-lite/encode/key-storage.h"
#include "ndn-lite/encode/ndn-rule-storage.h"
#include "ndn-lite/forwarder/pit.h"
#include "ndn-lite/forwarder/fib.h"
#include "ndn-lite/forwarder/forwarder.h"
#include "ndn-lite/util/uniform-time.h"
#include "ndn-lite/forwarder/face.h"

int main() {
    ndn_interest_t interest;
    ndn_name_t prefix_name;
    //DEMO: CHANGE
    char *ancmt_string = "/ancmt/1/1";
    ndn_name_from_string(&prefix_name, ancmt_string, strlen(ancmt_string));
    ndn_name_print(&prefix_name);
    
    return 0;
}