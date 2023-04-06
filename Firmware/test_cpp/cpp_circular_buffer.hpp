//
// Created by andre on 2/13/2023.
//

#ifndef JADE_3D_PRINTER_CPP_CIRCULAR_BUFFER_HPP
#define JADE_3D_PRINTER_CPP_CIRCULAR_BUFFER_HPP

#include <string>
#include <valarray>
#include <cstring>
#include <iostream>

#define NUM_ELEMENTS_PER_MESSAGE 9 // length of each message, including the added terminators
#define NUM_MESSAGES_IN_ARRAY 10  // total num messages that can be stored in array

class circular_buffer{
    private:
        int curr;
        int next;
        int length;  // actual num messages in array
        int num_messages;
        char buff[NUM_ELEMENTS_PER_MESSAGE * NUM_MESSAGES_IN_ARRAY];
    public:
        circular_buffer();
        int get_length();
        void enqueue(char *element);
        char *dequeue(char *dequeued_element);
        bool is_full();
        bool is_empty();
        // bool is_terminated();
};

circular_buffer::circular_buffer() {
    // constructor
    this->next = 0;
    this->curr = 0;
    this->num_messages = 0;
    this->length = strlen(this->buff);
}

int circular_buffer::get_length() {
    return this->length;
}

bool circular_buffer::is_empty() {
    return this->length == 0;
}

bool circular_buffer::is_full() {
    return this->num_messages == NUM_MESSAGES_IN_ARRAY;
}

void circular_buffer::enqueue(char *element) {
    if (this->is_full()) {
        exit(1);    // custom error handling? don't want to exit
    }
    strcat(this->buff, element);
    strcat(this->buff, "FFFF");
    this->next = this->next + strlen(element) + 4;  // next element is at current location + len of what we added + 4
    // for FFFF
    if(this->next == NUM_ELEMENTS_PER_MESSAGE * NUM_MESSAGES_IN_ARRAY){
        this->next = 0;
    }
    this->length++;
}

char *circular_buffer::dequeue(char *dequeued_element) {
    // memcpy(dequeued_element, this->buff + this->curr, NUM_ELEMENTS_PER_MESSAGE);
    // beginning of char array has initializer '\006' that needs to be ignored
    if(this->is_empty()){
        exit(1);
    }
    auto temp = std::begin(this->buff) + 1 + this->curr;
    std::copy(temp, temp + NUM_ELEMENTS_PER_MESSAGE, dequeued_element);
    this->length--;
    this->curr += NUM_ELEMENTS_PER_MESSAGE;
    return dequeued_element;
}

/*
bool circular_buffer::is_terminated() {
    if(std::strncpy() == "FFFF"){
        return true;
    }
    return false;
}
*/

#endif //JADE_3D_PRINTER_CPP_CIRCULAR_BUFFER_HPP
