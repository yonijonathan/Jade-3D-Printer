//
// Created by andre on 2/13/2023.
//

#include "cpp_circular_buffer.hpp"

int main(){
    circular_buffer cb;
    cb.enqueue("hello");
    cb.enqueue("abcde");
    cb.enqueue("value");
    cb.enqueue("cycle");
    cb.enqueue("three");
    cb.enqueue("hello");
    cb.enqueue("abcde");
    cb.enqueue("cycle");
    cb.enqueue("three");
    char dequeued[NUM_ELEMENTS_PER_MESSAGE];
    printf("dequeued: %s\n", cb.dequeue(dequeued));
    printf("dequeued: %s\n", cb.dequeue(dequeued));
    printf("dequeued: %s\n", cb.dequeue(dequeued));
    printf("dequeued: %s\n", cb.dequeue(dequeued));
    printf("dequeued: %s\n", cb.dequeue(dequeued));
    printf("dequeued: %s\n", cb.dequeue(dequeued));
    printf("dequeued: %s\n", cb.dequeue(dequeued));
    printf("dequeued: %s\n", cb.dequeue(dequeued));
    printf("dequeued: %s\n", cb.dequeue(dequeued));
    return 0;
}