#include <stdio.h>
//#include <glibc.h>
#include "circular_buffer.h"

char* decode_message(char **message){
    int init_str_length = strlen(message);
    int total_strings = BUFFER_SIZE;
    char *decoded_message = malloc(total_strings * sizeof(char *));
    decoded_message = message;
    return decoded_message;
}

void destroy_decoded_message(char **message){
    free(message);
}

int main(void){

    circular_buffer cb;
    init_buffer(&cb);

    char txt[] = "abcde";
    char txt2[] = "hello, world";
    char r[STR_SIZE];

    enqueue(&cb, txt);
    enqueue(&cb, txt2);
    dequeue(&cb, r);
    printf("first arr: %s\n", r);

    dequeue(&cb, r);
    printf("second arr: %s\n", r);

    return 0;
}