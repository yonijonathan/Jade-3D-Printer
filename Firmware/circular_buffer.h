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

char empty_index_value(char element[]){
    return *strcpy(element, NULL);
}

int is_empty(circular_buffer *buffer){
    return buffer->head == buffer->curr;
}

int is_full(circular_buffer *buffer){
    return (buffer->head + 1) % BUFFER_SIZE == buffer->curr;
}

void enqueue(circular_buffer *buffer, char *item){
    if(is_full(buffer)){
        exit(1);
    }
    strcpy(buffer->element[buffer->curr], item);
    buffer->head = (buffer->head + 1) % BUFFER_SIZE;
    buffer->length++;
}

char* dequeue(circular_buffer *buffer){
    static char removed_item[STR_SIZE];
    if(is_empty(buffer)){
        return NULL;
    }
    strcpy(removed_item, buffer->element[buffer->curr]);
    buffer->curr = (buffer->curr + 1) % BUFFER_SIZE;
    return removed_item;
}

#endif //JADE_3D_PRINTER_CIRCULAR_BUFFER_H
