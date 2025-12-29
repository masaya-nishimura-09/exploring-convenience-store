#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>
#define vertical 20
#define horizontal 50
#define max_items 10

int main(void) {
    
    time_t t = time(NULL);
	struct tm *local = localtime(&t);
    char now[50];
    sprintf(now, "./output/%04d-%02d-%02d_%02d-%02d-%02d.txt", local->tm_year + 1900, local->tm_mon + 1, local->tm_mday, local->tm_hour, local->tm_min, local->tm_sec);
    printf("%s\n", now);

    FILE *file;
    file = fopen(now, "w");
    fprintf(file, "test.c output data\n\n");


    // Fetch data from input files

    int starting_x = 0;
    int starting_y = 0;
    char shopping_list[max_items];
    char store[vertical][horizontal];

    FILE *starting_position_file;
    if ((starting_position_file = fopen("./input/starting_position.txt", "r")) == NULL) {
        printf("Can't open the file.");
    }
    else {
        fscanf(starting_position_file, "%d%d", &starting_x, &starting_y);
    }
    fclose(starting_position_file); 

    FILE *shopping_list_file;
    if ((shopping_list_file = fopen("./input/shopping_list.txt", "r")) == NULL) {
        printf("Can't open the file.");
    }
    else {
        for (int i = 0; fscanf(shopping_list_file, "%c", &shopping_list[i]) == 1; i++) {
            fscanf(shopping_list_file, "%c", &shopping_list[i]);
        }
    }
    fclose(shopping_list_file); 

    FILE *map_file;
    if ((map_file = fopen("./input/map.txt", "r")) == NULL) {
        printf("Can't open the file.");
    }
    else {
        for (int i = 0; i < vertical; i++) {
            fgets(store[i], horizontal + 2, map_file);
        }
    }
    fclose(map_file); 

    printf("(%d, %d)\n\n", starting_x, starting_y);

    for (int i = 0; i < max_items; i++) {
        if (shopping_list[i]) {
            printf("%c -> ", shopping_list[i]);
        }
    }

    printf("\n\n");

    
    for (int i = 0; i < vertical; i++) {
        for (int j = 0; j < horizontal; j++) {
            printf("%c", store[i][j]);
        }
        printf("\n"); 
    }
  
    return 0;
}