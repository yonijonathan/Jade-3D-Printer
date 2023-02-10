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
    enqueue(&cb, txt);
    enqueue(&cb, "fghijkl");
    // enqueue(&cb, 1121);
    // enqueue(&cb, 23498756);
    char *removed = dequeue(&cb);
    char *removed2 = dequeue(&cb);
    char *a = &removed[0];

    //printf("Dequeued: %s\n", removed);
    printf("first arr: %c\n", removed);
    printf("2nd arr: %c\n", removed2);

    //printf("second element: %c\n", removed[1]);
    //printf("third element: %c\n", removed[2]);
    //printf("fourth element: %c\n", removed[3]);
    //char *dm = decode_message(&removed);
    //printf("Message: %c", dm);
    //destroy_decoded_message(&dm);

    // printf("Dequeued: %d\n", dequeue(&cb));
    // printf("Dequeued: %d\n", dequeue(&cb));

    return 0;
}