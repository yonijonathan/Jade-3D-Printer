//
// Created by andre on 1/31/2023.
//

#ifndef JADE_3D_PRINTER_CIRCULAR_BUFFER_H
#define JADE_3D_PRINTER_CIRCULAR_BUFFER_H

#include <limits.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define BUFFER_SIZE 10
#define STR_SIZE 100

typedef struct
{
    int head; // where elements can be added to the buffer
    int curr; // current element of the buffer
    int length;
    char element[BUFFER_SIZE][STR_SIZE];
}circular_buffer;

void init_buffer(circular_buffer *buffer){
    buffer->head = 0;
    buffer->curr = 0;
    buffer->length = strlen(buffer->element);
}

int is_empty(circular_buffer *buffer){
    return buffer->length == 0;
}

int is_full(circular_buffer *buffer){
    return buffer->length == BUFFER_SIZE;
}

void enqueue(circular_buffer *buffer, char *item){
    if(is_full(buffer)){
        exit(1); // clean this up so that there is a more informational error. plus, we don't want to exit
    }
    strcpy(buffer->element[buffer->head], item);
    (buffer->head++) % BUFFER_SIZE;
    //(buffer->curr++) % BUFFER_SIZE;
    buffer->length++;
}

char* dequeue(circular_buffer *buffer){
    if(is_empty(buffer)){
        return NULL;
    }
    char removed_item[strlen(buffer->element[buffer->curr]+1)];
    strcpy(removed_item, buffer->element[buffer->curr]);
    (buffer->curr--) % BUFFER_SIZE;
    (buffer->head--) % BUFFER_SIZE;
    buffer->length--;
    return removed_item;
}

#endif //JADE_3D_PRINTER_CIRCULAR_BUFFER_H
