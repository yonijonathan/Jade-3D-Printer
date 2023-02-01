//
// Created by andre on 1/31/2023.
//

#ifndef JADE_3D_PRINTER_CIRCULAR_BUFFER_H
#define JADE_3D_PRINTER_CIRCULAR_BUFFER_H

#include <limits.h>

#define BUFFER_SIZE 10
#define EMPTY_INDEX_VAL INT_MAX


typedef struct
{
    int head; // where elements can be added to the buffer
    int curr; // current element of the buffer
    int buff[BUFFER_SIZE];
}circular_buffer;

void init_buffer(circular_buffer *buffer){
    buffer->head = 0;
    buffer->curr = 0;
    for(int i = 0; i < BUFFER_SIZE; i++){
        buffer->buff[i] = EMPTY_INDEX_VAL;
    }
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
    buffer->buff[buffer->curr] = EMPTY_INDEX_VAL;
    buffer->curr = (buffer->curr + 1) % BUFFER_SIZE;
    return item;
}

#endif //JADE_3D_PRINTER_CIRCULAR_BUFFER_H
