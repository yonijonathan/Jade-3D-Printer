#include <stdio.h>
#include <stdlib.h>

#define BUFFER_SIZE 10
#define EMPTY_BUFFER_INT INT_MAX

typedef struct
{
    int head; // where elements can be added to the buffer
    int curr; // current element of the buffer
    int buff[BUFFER_SIZE];
}circular_buffer;

void init_buffer(circular_buffer *buffer){
    buffer->head = 0; 
    buffer->curr = 0;
}

int is_empty(circular_buffer *buffer){
    return buffer->head == buffer->curr;
}

int is_full(circular_buffer *buffer){
    return (buffer->head + 1) % BUFFER_SIZE == buffer->curr;
}

void enqueue(circular_buffer *buffer, int item){
    if(is_full(buffer)){
        exit(1);
    }
    buffer->buff[buffer->head] = item;
    buffer->head = (buffer->head + 1) % BUFFER_SIZE;
}

int dequeue(circular_buffer *buffer){
    if(is_empty(buffer)){
        exit(1);
    }
    int item = buffer->buff[buffer->curr];
    buffer->buff[buffer->curr] = EMPTY_BUFFER_INT;
    buffer->curr = (buffer->curr + 1) % BUFFER_SIZE;
    return item;
}

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
