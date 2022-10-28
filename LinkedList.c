#include <stdio.h>
#include <stdlib.h>

typedef struct node {
   int data;
   struct node *next;   
} Node;

void create_list(Node **head);
void print_list(Node *head);
int insert(Node **head, int new_value);
int find(Node *head, int target);
int delete(Node **head, int value);

void create_list(Node **head) {
   *head = NULL;
}

/* Why not Node ** ? */
void print_list(Node *head) {
   if (!head) {
      printf("Empty list\n");
   } else {
      Node *current = head;
      while (current != NULL) {
         printf("%d ", current->data);

         current = current->next; 
      }
      printf("\n");
   }
}

int insert(Node **head, int new_value) {
   Node *current = *head, *prev = NULL, *new_item;

   while (current != NULL && new_value > current->data) {
      prev = current;
      current = current->next;
   }

   new_item = malloc(sizeof(Node));
   if (new_item == NULL) {
      return 0;
   }
   new_item->data = new_value;
   new_item->next = current;
   if (prev == NULL) { /* inserting at the beginning */ 
      *head = new_item;
   } else {
      prev->next = new_item;
   }

   return 1;
}

int find(Node *head, int target) {
   while (head != NULL && head->data != target) {
      head = head->next;
   }

   return head != NULL;
}

int delete(Node **head, int value) {
   Node *prev = NULL, *current = *head;

   while (current != NULL && current->data != value) {
      prev = current;
      current = current->next;
   }
   if (current == NULL){
      return 0;  /* not found */
   }
   if (prev == NULL) {
      *head = current->next;  /* deleted first item */
   } else {
      prev->next = current->next;
   }
   free(current);

   return 1;
}
