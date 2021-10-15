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
#include <netdb.h>
#include <sys/socket.h>
#include <arpa/inet.h>
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

#define PORT 8888
#define NODE1 "155.246.44.142"
#define NODE2 "155.246.215.101"
#define NODE3 "155.246.202.145"
#define NODE4 "155.246.216.113"
#define NODE5 "155.246.203.173"
#define NODE6 "155.246.216.39"
#define NODE7 "155.246.202.111"
#define NODE8 "155.246.212.111"
#define NODE9 "155.246.213.83"
#define NODE10 "155.246.210.98"
#define DEBUG "155.246.182.52"

//in the build directory go to make files and normal node -change the link.txt
//CMAKE again
//then make
//link.txt
///usr/bin/cc  -std=c11 -Werror -Wno-format -Wno-int-to-void-pointer-cast -Wno-int-to-pointer-cast -O3   CMakeFiles/normal-node.dir/examples/normal-node.c.o  -pthread -o examples/normal-node  libndn-lite.a

struct delay_struct {
    int struct_selector;
    ndn_interest_t interest;
};

//intitialize pit and fib for layer 1
ndn_pit_t *layer1_pit;
ndn_fib_t *router_fib;
ndn_fib_t *layer1_fib;
ndn_forwarder_t *router;
//char ip_address = "192.168.1.10";

//To start/stop main loop
bool running;

//To set whether this node is anchor
bool is_anchor = false;

//To set whether an announcement(interest) has been sent
bool ancmt_sent = false;

//Time Slice
int time_slice = 3;

//Selector integers
//selector will be set from hash function of previous block
uint8_t selector[10] = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}; //change from 0 to 9
uint8_t *selector_ptr = selector;
bool stored_selectors[10];

bool delay_start[10];
//clock time is in nano seconds, divide by 10^6 for actual time
int delay = 3000000;
int max_interfaces = 2;
//set array for multiple anchors for anchor/selector 1 - 10
int interface_num[10];
bool did_flood[10];

//
int last_interest;

//ndn keys
ndn_ecc_prv_t *ecc_secp256r1_prv_key;
ndn_ecc_pub_t *ecc_secp256r1_pub_key;
//ndn_key_storage_t *storage;

//Signature data for node (private key)
uint8_t secp256r1_prv_key_str[32] = {
0xA7, 0x58, 0x4C, 0xAB, 0xD3, 0x82, 0x82, 0x5B, 0x38, 0x9F, 0xA5, 0x45, 0x73, 0x00, 0x0A, 0x32,
0x42, 0x7C, 0x12, 0x2F, 0x42, 0x4D, 0xB2, 0xAD, 0x49, 0x8C, 0x8D, 0xBF, 0x80, 0xC9, 0x36, 0xB5
};

//Signature data for node (puplic key)
uint8_t secp256r1_pub_key_str[64] = {
0x99, 0x26, 0xD6, 0xCE, 0xF8, 0x39, 0x0A, 0x05, 0xD1, 0x8C, 0x10, 0xAE, 0xEF, 0x3C, 0x2A, 0x3C,
0x56, 0x06, 0xC4, 0x46, 0x0C, 0xE9, 0xE5, 0xE7, 0xE6, 0x04, 0x26, 0x43, 0x13, 0x8A, 0x3E, 0xD4,
0x6E, 0xBE, 0x0F, 0xD2, 0xA2, 0x05, 0x0F, 0x00, 0xAC, 0x6F, 0x5D, 0x4B, 0x29, 0x77, 0x2D, 0x54,
0x32, 0x27, 0xDC, 0x05, 0x77, 0xA7, 0xDC, 0xE0, 0xA2, 0x69, 0xC8, 0x8B, 0x4C, 0xBF, 0x25, 0xF2
};

//socket variables
int sock = 0, valread;
struct sockaddr_in serv_addr;
char *debug_message;
char buffer[1024] = {0};

ndn_udp_face_t *face1, *face2, *face3, *face4, *face5, *face6, *face7, *face8, *face9, *face10, *data_face;

int send_debug_message(char *input) {
    debug_message = input;
    send(sock , debug_message, strlen(debug_message) , 0 );

    //printf("Hello message sent\n");
    //valread = read( sock , buffer, 1024);
    //printf("%s\n",buffer);
    return 0;
}

//may have to use interest as a pointer
void flood(ndn_interest_t interest_pkt) {
    printf("\nFlooding\n");
    ndn_interest_t interest;
    ndn_name_t prefix_name;
    //DEMO: CHANGE
    char *ancmt_string = "/ancmt/1/9";
    ndn_name_from_string(&prefix_name, ancmt_string, strlen(ancmt_string));

    uint8_t selector[10] = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9};
    uint8_t *selector_ptr = selector;
    ndn_udp_face_t *face;
    
    //myip, my outgoing port, their incoming ip, their incoming port
    in_port_t port1, port2;
    in_addr_t server_ip;
    char *sz_port1, *sz_port2, *sz_addr;
    uint32_t ul_port;
    struct hostent * host_addr;
    struct in_addr ** paddrs;
    
    //char *prefix = &interest.name.components[0].value[0];
    //printf("Prefix Old: %s\n", prefix);
    
    //prefix = &interest.name.components[0].value[0];
    //printf("Prefix New: %s\n", prefix);
    
    //gets the forwarder intiailized in the main message
    //router_const = ndn_forwarder_get();
    //router = ndn_forwarder_get();

    //Layer 1 Data Packet
    if(is_anchor) {
        //Anchor flooding announcement (layer 1)
        //Flood without accounting for time delay or max number of interfaces
        //Get all closest interfaces and forward to them
        printf("Forwarding Announcement (Anchor)\n");
        //insert fib information here
        
        // for(int i = 0; i < ndn_forwarder_get().fib.capacity; i ++) {
        //     //printf("looking at interfaces in fib")
        //     ndn_forwarder_express_interest_struct(&interest, on_data, NULL, NULL);
        // }
    }

    else {
        //Normal node flooding announcement (layer 1)
        //Flood while using time delay and accounting for interfaces
        //check pit for incoming interest, then send out interest for each not in pit
        //layer1_fib = router->fib;
        printf("Forwarding Announcement (Non-Anchor)\n");
        //printf("PIT Entires: %d\n", sizeof(router->pit->slots));
        // for(int i = 0; i < router->pit->capacity; i++) {
        //     printf("Iterate number: %d\n", i);
        //     ndn_table_id_t temp_pit_id = router->pit->slots[i].nametree_id;
        //     nametree_entry_t *temp_nametree_entry = ndn_nametree_at(router->nametree, temp_pit_id);
        //     printf("Here\n");
        //     ndn_table_id_t temp_fib_id = temp_nametree_entry->fib_id;
        //     //TODO: Segmentation Fault Here
        //     ndn_fib_unregister_face(router->fib, temp_fib_id);
        // }
        //router->fib = layer1_fib;        

        //DEMO: CHANGE
        //Node2-Anchor
        sz_port1 = "3000";
        sz_addr = NODE10;
        sz_port2 = "5000";
        host_addr = gethostbyname(sz_addr);
        paddrs = (struct in_addr **)host_addr->h_addr_list;
        server_ip = paddrs[0]->s_addr;
        ul_port = strtoul(sz_port1, NULL, 10);
        port1 = htons((uint16_t) ul_port);
        ul_port = strtoul(sz_port2, NULL, 10);
        port2 = htons((uint16_t) ul_port);
        face = ndn_udp_unicast_face_construct(INADDR_ANY, port1, server_ip, port2);
        ndn_forwarder_add_route_by_name(&face->intf, &prefix_name);

        ndn_interest_from_name(&interest, &prefix_name);
        ndn_interest_set_Parameters(&interest, (uint8_t*)(selector_ptr + 1), sizeof(selector[1]));
        ndn_forwarder_express_interest_struct(&interest, NULL, NULL, NULL);

        // for(int i = 0; i < layer1_fib.capacity; i++) {
        //     ndn_forwarder_express_interest_struct(&interest, on_data, NULL, NULL);
        // }
    }

    printf("Flooded Interest!\n");
    send_debug_message("Flooded Interest");
}

void send_ancmt() {
    printf("\nSending Announcement...\n");

    //include periodic subscribe of send_anct
    //ndn_interest_t *ancmt = new ndn_interest_t();
    //malloc
    ndn_interest_t ancmt;
    ndn_encoder_t encoder;
    ndn_udp_face_t *face;
    ndn_name_t prefix_name;
    char *prefix_string = "/ancmt/1";
    char interest_buf[4096];

    //. instead ->, initialize as a pointer object first, testing new keyword

    //Sets timestamp
    //time_t clk = time(NULL);
    //char* timestamp = ctime(&clk);

    //This creates the routes for the interest and sends to nodes
    //ndn_forwarder_add_route_by_name(&face->intf, &prefix_name);
    ndn_name_from_string(&prefix_name, prefix_string, strlen(prefix_string));
    //FIXED TODO: Segmentation Fault Here
    ndn_interest_from_name(&ancmt, &prefix_name);
    //ndn_forwarder_express_interest_struct(&interest, on_data, on_timeout, NULL);

    //gets ndn (timestamp)
    ndn_time_ms_t timestamp = ndn_time_now_ms();

    //parameter may be one whole string so the parameters may have to be sorted and stored in a way that is readabel by other normal nodes
    //Init ancmt with selector, signature, and timestamp
    //may have to use ex: (uint8_t*)str for middle param
    
    ndn_interest_set_Parameters(&ancmt, (uint8_t*)&timestamp, sizeof(timestamp));
    ndn_interest_set_Parameters(&ancmt, (uint8_t*)(selector_ptr + 1), sizeof(selector[1]));
    //ndn_interest_set_Parameters(&ancmt, (uint8_t*)ip_address, sizeof(ip_address));

    //Signed interest init
    ndn_key_storage_get_empty_ecc_key(&ecc_secp256r1_pub_key, &ecc_secp256r1_prv_key);
    ndn_ecc_make_key(ecc_secp256r1_pub_key, ecc_secp256r1_prv_key, NDN_ECDSA_CURVE_SECP256R1, 890);
    ndn_ecc_prv_init(ecc_secp256r1_prv_key, secp256r1_prv_key_str, sizeof(secp256r1_prv_key_str), NDN_ECDSA_CURVE_SECP256R1, 0);
    ndn_key_storage_t *storage = ndn_key_storage_get_instance();
    ndn_name_t *self_identity_ptr = storage->self_identity;
    //FIXED TODO: segmentation fault here
    ndn_signed_interest_ecdsa_sign(&ancmt, self_identity_ptr, ecc_secp256r1_prv_key);
    // encoder_init(&encoder, interest_buf, 4096);
    // //FIXED TODO: Segmentation Fault Here
    // ndn_interest_tlv_encode(&encoder, &ancmt);

    //uncomment here to test flood
    flood(ancmt);
    ancmt_sent = true;
    printf("Announcement sent.\n");
    //send_debug_message("Announcment Sent");
}

bool verify_interest(ndn_interest_t *interest) {
    printf("\nVerifying Packet\n");
    //check signature is correct from the public key is valid for all normal nodes
    //check if timestamp is before the current time
    int timestamp = interest->parameters.value[0];
    int current_time = ndn_time_now_ms();
    //verify time slot

    if((current_time - timestamp) < 0) {
        return false;
    }
    else if(ndn_signed_interest_ecdsa_verify(interest, ecc_secp256r1_pub_key) != NDN_SUCCESS) {
        return false;
    }
    //send_debug_message("Interest Verified");
    return true;
}

void reply_ancmt() {
    //send_debug_message("Announcent Reply Sent");
    //look at find 
}

/*
void insert_pit(ndn_interest_t interest) {
    //send_debug_message("Packet Inserted Into PIT");
    router = ndn_forwarder_get();
    layer1_pit = router->pit;
    uint8_t* name;
    ndn_pit_find_or_insert(layer1_pit, interest, &interest.name.components.value, &interest.name.components_size);
}
*/

void *start_delay(void *arguments) {
    printf("\nDelay started\n");
    struct delay_struct *args = arguments;
    //starts delay and adds onto max interfaces
    clock_t start_time = clock();
    printf("Delay Time: %d seconds\n", delay/1000000);
    while (clock() < start_time + delay) {
    }
    printf("Delay Complete\n");
    //then when finished, flood
    if(did_flood[args->struct_selector] == true) {
        printf("Already flooded\n");
    } 
    else {
        flood(args->interest);
        did_flood[args->struct_selector] = true;
        reply_ancmt();
        //pthread_exit(NULL);
    }
}

char *trimwhitespace(char *str) {
    char *end;

    while(isspace((unsigned char)*str)) str++;

    if(*str == 0)
    return str;

    end = str + strlen(str) - 1;
    while(end > str && isspace((unsigned char)*end)) end--;

    end[1] = '\0';

    return str;
}

void generate_data() {
    //sends data anchor direction (layer1)
    //using different port because dont know if prefix name will interfere with ndn_forwarder for sending data
    printf("Generate Data\n");
    ndn_data_t data;
    ndn_encoder_t encoder;
    char *str = "This is Layer 1 Data Packet";
    uint8_t buf[4096];

    ndn_name_t prefix_name;
    //prefix string can be anything here because data_recieve bypasses prefix check in fwd_data_pipeline
    char *prefix_string = "/l1data/1/8";
    ndn_name_from_string(&prefix_name, prefix_string, strlen(prefix_string));

    data.name = prefix_name;
    ndn_data_set_content(&data, (uint8_t*)str, strlen(str) + 1);
    ndn_metainfo_init(&data.metainfo);
    ndn_metainfo_set_content_type(&data.metainfo, NDN_CONTENT_TYPE_BLOB);
    encoder_init(&encoder, buf, 4096);
    ndn_data_tlv_encode_digest_sign(&encoder, &data);
    ndn_face_send(&data_face->intf, encoder.output_value, encoder.offset);

    send_debug_message("Data Sent");
}

//is this threaded
//non zero chance of flooding twice due to multithreading
int on_interest(const uint8_t* interest, uint32_t interest_size, void* userdata) {
    printf("\nNormal-Node On Interest\n");
    pthread_t layer1;
    ndn_interest_t interest_pkt;
    ndn_interest_from_block(&interest_pkt, interest, interest_size);

    char *prefix = &interest_pkt.name.components[0].value[0];
    prefix = trimwhitespace(prefix);
    printf("PREFIX: /%s/", prefix);
    prefix = &interest_pkt.name.components[1].value[0];
    prefix = trimwhitespace(prefix);
    printf("%s/", prefix);
    prefix = &interest_pkt.name.components[2].value[0];
    prefix = trimwhitespace(prefix);
    printf("%s\n", prefix);

    if(strcmp(prefix, "1") == 0) {
        printf("On Data Interface: %s", prefix);
        data_face = face1;
    }
    else if(strcmp(prefix, "2") == 0) {
        printf("On Data Interface: %s", prefix);
        data_face = face2;
    }
    else if(strcmp(prefix, "3") == 0) {
        printf("On Data Interface: %s", prefix);
        data_face = face3;
    }
    else if(strcmp(prefix, "4") == 0) {
        printf("On Data Interface: %s", prefix);
        data_face = face4;
    }
    else if(strcmp(prefix, "5") == 0) {
        printf("On Data Interface: %s", prefix);
        data_face = face5;
    }
    else if(strcmp(prefix, "6") == 0) {
        printf("On Data Interface: %s", prefix);
        data_face = face6;
    }
    else if(strcmp(prefix, "7") == 0) {
        printf("On Data Interface: %s", prefix);
        data_face = face7;
    }
    else if(strcmp(prefix, "8") == 0) {
        printf("On Data Interface: %s", prefix);
        data_face = face8;
    }
    else if(strcmp(prefix, "9") == 0) {
        printf("On Data Interface: %s", prefix);
        data_face = face9;
    }
    else if(strcmp(prefix, "10") == 0) {
        printf("On Data Interface: %s", prefix);
        data_face = face10;
    }

    //TODO: make this a function later
    //strcat requires an array of dedicated size
    prefix = &interest_pkt.name.components[2].value[0];
    prefix = trimwhitespace(prefix);
    char temp_message[80];
    strcat(temp_message, "On Interest: ");
    strcat(temp_message, prefix);
    strcat(temp_message, " ");
    send_debug_message(temp_message);

    prefix = &interest_pkt.name.components[0].value[0];
    prefix = trimwhitespace(prefix);
    prefix = "ancmt";

    // for (int i = 0; i < interest_pkt.name.components_size; i++) {
    //     printf("/");
    //     for (int j = 0; j < interest_pkt.name.components[i].size; j++) {
    //         printf("%c", interest_pkt.name.components[i].value[j]);
    //     }
    // }
    // printf("\n");

    int timestamp = interest_pkt.parameters.value[0];
    printf("TIMESTAMP: %d\n", timestamp);
    int current_time = ndn_time_now_ms();
    printf("LAST INTEREST: %d\n", last_interest);
    
    //selector number
    int parameters = interest_pkt.parameters.value[0];
    printf("SELECTOR: %d\n", parameters);
    printf("STORED SELECTOR: %d\n", stored_selectors[parameters]);

    struct delay_struct args;
    args.interest = interest_pkt;
    args.struct_selector = parameters;
    
    //printf("%s\n", prefix);

    //make sure to uncomment verify 
    // if(verify_interest(&interest_pkt) == false) {
    //     printf("Packet Wrong Format!");
    //     return NDN_UNSUPPORTED_FORMAT;
    // }
    //printf("Packet Verified!\n");

    //check ancmt, stored selectors, and timestamp(maybe)
    //timestamp + selector for new and old
    //TODO: fix time to coorespond to last ancmt timestamp
    //if((prefix == "ancmt") && stored_selectors[parameters] == false && (timestamp - last_interest) > 0) {
    if(strcmp(prefix, "ancmt") == 0 && stored_selectors[parameters] == false) {
        printf("New Ancmt\n");
        stored_selectors[parameters] = true;
        if(delay_start[parameters] != true) {
            pthread_create(&layer1, NULL, &start_delay, (void *)&args);
            delay_start[parameters] = true;
        }
        interface_num[parameters]++;

        //insert_pit(interest_pkt);
        //call insert pit here as well for first case scenario
        // if(interface_num[parameters] >= max_interfaces) {
        //    flood(interest_pkt);
        //    did_flood[parameters] = true;
        //    reply_ancmt();
        // }
    }

    else if(strcmp(prefix, "ancmt") == 0 && stored_selectors[parameters] == true) {
        printf("Old Ancmt\n");
        interface_num[parameters]++;
        if(did_flood[parameters] == true) {
            printf("Already flooded\n");
        }
        else if(interface_num[parameters] >= max_interfaces) {
            if(did_flood[parameters] == true) {
                printf("Already flooded\n");
            }
            else {
                //should call insert pit here and the start delay function
                flood(interest_pkt);
                printf("Maximum Interfaces Reached\n");
                did_flood[parameters] = true;
                reply_ancmt();
                //pthread_exit(NULL);
            }
        }
    }

    last_interest = current_time;
    printf("END OF ON_INTEREST\n");

    //DEMO: CHANGE
    //this is for producer generate data fter 6 second delay
    /*
    clock_t timer = clock();
    printf("Delay Time: %d seconds\n", 6);
    while (clock() < (timer + 6000000)) {
    }
    */

    return NDN_FWD_STRATEGY_SUPPRESS;
}

//how do i populate the fib
//how do i populate the pit
//how do you send an interest to set of given entries inside pit of fib

void populate_incoming_fib() {
    //NOTE: for recieving an incoming interest packet change the prefix string to the nodes that you want to recieve from
    //also to send a interest packet, change the outgoing interest packet prefix
    printf("\nIncoming FIB populated\nNOTE: all other nodes must be turned on and in the network, else SegFault \n");
    char *ancmt_string;
    ndn_name_t name_prefix;
    ndn_udp_face_t *face;

    in_port_t port1, port2;
    in_addr_t server_ip;
    char *sz_port1, *sz_port2, *sz_addr;
    uint32_t ul_port;
    struct hostent * host_addr;
    struct in_addr ** paddrs;

    
    //DEMO: CHANGE
    //remove youre own incoming interface
    //change NODE(NUM) and face(num)
    //Node1-Anchor
    sz_port1 = "5000";
    sz_addr = NODE1;
    sz_port2 = "3000";
    host_addr = gethostbyname(sz_addr);
    paddrs = (struct in_addr **)host_addr->h_addr_list;
    server_ip = paddrs[0]->s_addr;
    ul_port = strtoul(sz_port1, NULL, 10);
    port1 = htons((uint16_t) ul_port);
    ul_port = strtoul(sz_port2, NULL, 10);
    port2 = htons((uint16_t) ul_port);
    face1 = ndn_udp_unicast_face_construct(INADDR_ANY, port1, server_ip, port2);

    //Node2-Anchor
    sz_port1 = "5000";
    sz_addr = NODE2;
    sz_port2 = "3000";
    host_addr = gethostbyname(sz_addr);
    paddrs = (struct in_addr **)host_addr->h_addr_list;
    server_ip = paddrs[0]->s_addr;
    ul_port = strtoul(sz_port1, NULL, 10);
    port1 = htons((uint16_t) ul_port);
    ul_port = strtoul(sz_port2, NULL, 10);
    port2 = htons((uint16_t) ul_port);
    face2 = ndn_udp_unicast_face_construct(INADDR_ANY, port1, server_ip, port2);

    //Node3-Anchor
    sz_port1 = "5000";
    sz_addr = NODE3;
    sz_port2 = "3000";
    host_addr = gethostbyname(sz_addr);
    paddrs = (struct in_addr **)host_addr->h_addr_list;
    server_ip = paddrs[0]->s_addr;
    ul_port = strtoul(sz_port1, NULL, 10);
    port1 = htons((uint16_t) ul_port);
    ul_port = strtoul(sz_port2, NULL, 10);
    port2 = htons((uint16_t) ul_port);
    face3 = ndn_udp_unicast_face_construct(INADDR_ANY, port1, server_ip, port2);

    //Node4-Anchor
    sz_port1 = "5000";
    sz_addr = NODE4;
    sz_port2 = "3000";
    host_addr = gethostbyname(sz_addr);
    paddrs = (struct in_addr **)host_addr->h_addr_list;
    server_ip = paddrs[0]->s_addr;
    ul_port = strtoul(sz_port1, NULL, 10);
    port1 = htons((uint16_t) ul_port);
    ul_port = strtoul(sz_port2, NULL, 10);
    port2 = htons((uint16_t) ul_port);
    face4 = ndn_udp_unicast_face_construct(INADDR_ANY, port1, server_ip, port2);

    //Node5-Anchor
    sz_port1 = "5000";
    sz_addr = NODE5;
    sz_port2 = "3000";
    host_addr = gethostbyname(sz_addr);
    paddrs = (struct in_addr **)host_addr->h_addr_list;
    server_ip = paddrs[0]->s_addr;
    ul_port = strtoul(sz_port1, NULL, 10);
    port1 = htons((uint16_t) ul_port);
    ul_port = strtoul(sz_port2, NULL, 10);
    port2 = htons((uint16_t) ul_port);
    face5 = ndn_udp_unicast_face_construct(INADDR_ANY, port1, server_ip, port2);

    //Node6-Anchor
    sz_port1 = "5000";
    sz_addr = NODE6;
    sz_port2 = "3000";
    host_addr = gethostbyname(sz_addr);
    paddrs = (struct in_addr **)host_addr->h_addr_list;
    server_ip = paddrs[0]->s_addr;
    ul_port = strtoul(sz_port1, NULL, 10);
    port1 = htons((uint16_t) ul_port);
    ul_port = strtoul(sz_port2, NULL, 10);
    port2 = htons((uint16_t) ul_port);
    face6 = ndn_udp_unicast_face_construct(INADDR_ANY, port1, server_ip, port2);

    //Node7-Anchor
    sz_port1 = "5000";
    sz_addr = NODE7;
    sz_port2 = "3000";
    host_addr = gethostbyname(sz_addr);
    paddrs = (struct in_addr **)host_addr->h_addr_list;
    server_ip = paddrs[0]->s_addr;
    ul_port = strtoul(sz_port1, NULL, 10);
    port1 = htons((uint16_t) ul_port);
    ul_port = strtoul(sz_port2, NULL, 10);
    port2 = htons((uint16_t) ul_port);
    face7 = ndn_udp_unicast_face_construct(INADDR_ANY, port1, server_ip, port2);

    //Node8-Anchor
    sz_port1 = "5000";
    sz_addr = NODE8;
    sz_port2 = "3000";
    host_addr = gethostbyname(sz_addr);
    paddrs = (struct in_addr **)host_addr->h_addr_list;
    server_ip = paddrs[0]->s_addr;
    ul_port = strtoul(sz_port1, NULL, 10);
    port1 = htons((uint16_t) ul_port);
    ul_port = strtoul(sz_port2, NULL, 10);
    port2 = htons((uint16_t) ul_port);
    face8 = ndn_udp_unicast_face_construct(INADDR_ANY, port1, server_ip, port2);


    //Node10-Anchor
    sz_port1 = "5000";
    sz_addr = NODE10;
    sz_port2 = "3000";
    host_addr = gethostbyname(sz_addr);
    paddrs = (struct in_addr **)host_addr->h_addr_list;
    server_ip = paddrs[0]->s_addr;
    ul_port = strtoul(sz_port1, NULL, 10);
    port1 = htons((uint16_t) ul_port);
    ul_port = strtoul(sz_port2, NULL, 10);
    port2 = htons((uint16_t) ul_port);
    face10 = ndn_udp_unicast_face_construct(INADDR_ANY, port1, server_ip, port2);

    //DEMO: CHANGE
    ancmt_string = "/ancmt/1/6";
    ndn_name_from_string(&name_prefix, ancmt_string, strlen(ancmt_string));
    ndn_forwarder_register_name_prefix(&name_prefix, on_interest, NULL);

    ancmt_string = "/ancmt/1/7";
    ndn_name_from_string(&name_prefix, ancmt_string, strlen(ancmt_string));
    ndn_forwarder_register_name_prefix(&name_prefix, on_interest, NULL);
}

void on_data(const uint8_t* rawdata, uint32_t data_size, void* userdata) {
    printf("On data\n");
    send_debug_message("On Data");

    ndn_data_t data;
    char *prefix = &data.name.components[0].value[0];
    
    if (ndn_data_tlv_decode_digest_verify(&data, rawdata, data_size)) {
        printf("Decoding failed.\n");
    }

    printf("DATA PREFIX: %s\n", prefix);
    printf("It says: %s\n", data.content_value);

    clock_t timer = clock();
    printf("Delay Time: %d seconds\n", 1);
    while (clock() < (timer + 1000000)) {
    }

    generate_data();
}

//interest is saved in pit until put-Data is called
/*
bool verify_data(ndn_data_t *data_pkt, const uint8_t* rawdata, uint32_t data_size) {
    printf("\nVerifying Packet\n");
    //check signature is correct from the public key is valid for all normal nodes
    //check if timestamp is before the current time
    int timestamp = data_pkt->signature.timestamp;
    int current_time = ndn_time_now_ms();
    //verify time slot

    if((current_time - timestamp) < 0) {
        return false;
    }

    else if(ndn_data_tlv_decode_ecdsa_verify(data_pkt, rawdata, data_size, ecc_secp256r1_pub_key) != NDN_SUCCESS) {
        return false;
    }

    send_debug_message("Data Verified");
    return true;
}

void reply_interest(ndn_data_t *data_pkt, int layer_num) {
    
}

bool check_CS(ndn_data_t *data_pkt) {

}

void on_data(const uint8_t* rawdata, uint32_t data_size, void* userdata) {
    ndn_data_t *data_pkt;
    ndn_data_t *vector;
    char *data_content;
    char *traverse;
    int layer_num;
    uint64_t *timestamp;//uint64_t
    // contentFormat: /data/layerNum/content

    if (ndn_data_tlv_decode_digest_verify(&data_pkt, rawdata, data_size)) {
        printf("Decoding failed\n");
    }

    // if(verify_data(&data_pkt, rawdata, data_size) == false) {
    //     return;
    // }

    data_content = data_pkt->content_value;//uint8
    timestamp = data_pkt->signature->timestamp;

    for(traverse = data_content; *traverse != '\0'; traverse++) {
        if((traverse - '0') == 1 || (traverse - '0') == 2) {
            layer_num = traverse - '0';
        }
    }
    if(layer_num == 1) {
        if(only_normal) {
            reply_interest(data_pkt, 1);
        }
        else {
            reply_interest(data_pkt, 1);
            data_pkt = attaching_vector();
            reply_interest(data_pkt, 2);
        }
    }
    if(layer_num == 2) {
        if(!check_CS(data_pkt)) {
            printf("Check CS fail\n");
        }
        vector = update_vector();
        if() {
            send_update_vector();
        }
        else {
            reply_interest(data_pkt, 2);
        }
    }
 
    printf("It says: %s\n", data_pkt.content_value);
    generate_data();
}

void select_anchor() {

}
*/

int main(int argc, char *argv[]) {
    printf("Main Loop\n");
    printf("Maximum Interfaces: %d\n", max_interfaces);

    //DEMO: CHANGE
    int node_num = 9;

    //socket connection
    if ((sock = socket(AF_INET, SOCK_STREAM, 0)) < 0)
    {
        printf("\n Socket creation error \n");
        return -1;
    }
   
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(PORT);

    if(inet_pton(AF_INET, DEBUG, &serv_addr.sin_addr)<=0) 
    {
        printf("\nInvalid address/ Address not supported \n");
        return -1;
    }
   
    if (connect(sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0)
    {
        printf("\nConnection Failed \n");
        return -1;
    }

    //TODO: make this a function later
    char temp_message[80];
    char temp_num[10];
    strcat(temp_message, "Node Start: ");
    sprintf(temp_num, "%d", node_num);
    strcat(temp_message, temp_num);
    send_debug_message(temp_message);
    
    ndn_lite_startup();

    last_interest = ndn_time_now_ms();
    
    //FACE NEEDS TO BE INITIATED WITH CORRECT PARAMETERS BEFORE SENDING OR RECEIVING ANCMT
    //DEMO: CHANGE
    populate_incoming_fib();
    callback_insert(on_data);
    //registers ancmt prefix with the forwarder so when ndn_forwarder_process is called, it will call the function on_interest
    //populate_outgoing_fib();

    //signature init

    //DEMO: CHANGE
    //is_anchor = true;
    if(is_anchor == true) {
        send_debug_message("Is Anchor");
    }

    running = true;
    while (running) {
        //uncomment here to test send anct
        if(is_anchor && !ancmt_sent) {
            //printf("send anct called\n");
            ndn_interest_t interest;
            flood(interest);
            //populate_outgoing_fib();
            ancmt_sent = true;
        }
        
        ndn_forwarder_process();
        usleep(10000);
    }
    //ndn_face_destroy(&face->intf);

    return 0;
}