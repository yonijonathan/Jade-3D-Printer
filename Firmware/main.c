#include <stdio.h>
#include "circular_buffer.h"

int main(void){
    circular_buffer cb;
    init_buffer(&cb);
    char txt[] = "abcde";
    enqueue(&cb, txt);
    // enqueue(&cb, 1121);
    // enqueue(&cb, 23498756);
    char *removed = dequeue(&cb);
    char *a = &removed[0];
    printf("Dequeued: %s\n", removed);
    printf("first element: %c\n", removed[0]);
    printf("second element: %c\n", removed[1]);
    printf("third element: %c\n", removed[2]);
    printf("fourth element: %c\n", removed[3]);

    // printf("Dequeued: %d\n", dequeue(&cb));
    // printf("Dequeued: %d\n", dequeue(&cb));

    return 0;
}