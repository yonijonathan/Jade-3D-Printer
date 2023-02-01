#include <stdio.h>
#include <stdlib.h>
#include "circular_buffer.h"

int main(void){
    circular_buffer cb;
    init_buffer(&cb);

    enqueue(&cb, 1000);
    enqueue(&cb, 1121);
    enqueue(&cb, 23498756);

    printf("Dequeued: %d\n", dequeue(&cb));
    printf("Dequeued: %d\n", dequeue(&cb));
    printf("Dequeued: %d\n", dequeue(&cb));

    return 0;
}