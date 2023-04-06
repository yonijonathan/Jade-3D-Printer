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
    int next; // where elements can be added to the buffer
    int curr; // current elements of the buffer
    int length; // length of array occupied by an elements
    char elements[BUFFER_SIZE][STR_SIZE];
}circular_buffer;

void init_buffer(circular_buffer *buffer){
    buffer->next = 0;
    buffer->curr = 0;
    buffer->length = strlen(buffer->elements);
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
    strcpy(buffer->elements[buffer->next], item);
    (buffer->next++) % BUFFER_SIZE;
    //(buffer->curr++) % BUFFER_SIZE;
    buffer->length++;
}

void dequeue(circular_buffer *buffer, char *removed_arr){
    if(is_empty(buffer)){
        // return NULL;
    }
    strcpy(removed_arr, buffer->elements[buffer->curr]);
    (buffer->curr++) % BUFFER_SIZE;
    buffer->length--;
}

#endif //JADE_3D_PRINTER_CIRCULAR_BUFFER_H
