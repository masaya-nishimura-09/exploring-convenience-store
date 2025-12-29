#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>
#define vertical 20
#define horizontal 50
#define max_items 1

struct Position {
    int x;
    int y; 
    int d;
    int px;
    int py;
    int pd;
    int steps;
    int progress;
};

int q_random() {
    int e = rand() % 10;
    if (e < 2) {
        return 0;
    }
    else {
        return 1;
    }
}

int cart_checker(char item, char cart[max_items]) {
    int already_picked = 0;
    for (int i = 0; i < max_items; i++) {
        if (item == cart[i]) {
            already_picked = 1;
            break;
        }
        if (cart[i] == '\0') {
            cart[i] = item;
            break;
        }
    }
    return already_picked;
}

int item_checker(char item, char shopping_list[max_items], char cart[max_items]) {
    int pick = 0;
    for (int i = 0; i < max_items; i++) {
        if (item == shopping_list[i]) {
            pick = 1;
        }
    }
    if (pick == 1) {
        int picked_or_not = cart_checker(item, cart);
        if (picked_or_not == 1) {
            pick = 0;
        } 
    }
    return pick;
}

void write_q(
    float q[vertical][horizontal][4], 
    char* urls[4]){

    FILE *write_file;

    for (int k = 0; k < 4; k++) {
        write_file = fopen(urls[k], "w");
        for (int i = 0; i < vertical; i++) {
            for (int j = 0; j < horizontal; j++) {
                fprintf(write_file, "%f ", q[i][j][k]);
            }
            fprintf(write_file, "\n");
        }
        fclose(write_file); 
    }
}

void read_q(
    float q[vertical][horizontal][4], 
    char* urls[4]) {

    FILE *read_file;

    for (int k = 0; k < 4; k++) {
        read_file = fopen(urls[k], "r");

        for (int i = 0; i < vertical; i++) {
            for (int j = 0; j < horizontal; j++) {
                fscanf(read_file, "%f", &q[i][j][k]);
            }            
        }
        fclose(read_file); 
    }
}

struct Position walk(
    char store[vertical][horizontal], 
    char shopping_list[max_items], 
    char cart[max_items], 
    FILE *file, 
    float sq[vertical][horizontal][4], 
    float iq[vertical][horizontal][4], 
    float cq[vertical][horizontal][4], 
    struct Position position
) {
    struct Position next_position;

    int next_direction = rand() % 4;
    if (q_random() == 1) {
        float value = 0;
        int q_number = 0;
        if (position.progress == 0) {
            for (int i = 0; i < 4; i++) {
                if (value < sq[position.x][position.y][i]) {
                    value = sq[position.x][position.y][i];
                    q_number = i;
                }
            }
        }
        else if (position.progress == 1) {
            for (int i = 0; i < 4; i++) {
                if (value < iq[position.x][position.y][i]) {
                    value = iq[position.x][position.y][i];
                    q_number = i;
                }
            }
        }
        else {
            for (int i = 0; i < 4; i++) {
                if (value < cq[position.x][position.y][i]) {
                    value = cq[position.x][position.y][i];
                    q_number = i;
                }
            }
        }
        
        if (value != 0) {
            next_direction = q_number;
        }
    }

    int next_x = 0;
    int next_y = 0;
    if (next_direction == 0) {
        next_x = position.x - 1;
        next_y = position.y;
    }
    else if (next_direction == 1) {
        next_x = position.x;
        next_y = position.y + 1;
    }
    else if (next_direction == 2) {
        next_x = position.x + 1;
        next_y = position.y;
    }
    else {
        next_x = position.x;
        next_y = position.y - 1;
    }

    if (next_x >= 0 && next_y >= 0 && next_x < vertical && next_y < horizontal){
        if (store[next_x][next_y] == ' ' || store[next_x][next_y] == '*') {
            store[next_x][next_y] = '*';
            next_position.x = next_x;
            next_position.y = next_y;
            next_position.px = position.x;
            next_position.py = position.y;
            next_position.pd = next_direction;
            next_position.steps = position.steps + 1;
            next_position.progress = position.progress;
            if (position.progress == 0) {
                if (sq[position.x][position.y][next_direction] > sq[position.px][position.py][position.pd]) {
                    sq[position.px][position.py][position.pd] = sq[position.x][position.y][next_direction] * 0.9;
                }
            }
            else if (position.progress == 1) {
                if (iq[position.x][position.y][next_direction] > iq[position.px][position.py][position.pd]) {
                    iq[position.px][position.py][position.pd] = iq[position.x][position.y][next_direction] * 0.9;
                }
            }
            else if (position.progress == 2) {
                if (cq[position.x][position.y][next_direction] > cq[position.px][position.py][position.pd]) {
                    cq[position.px][position.py][position.pd] = cq[position.x][position.y][next_direction] * 0.9;
                }
            }
            printf("\n(%d, %d)", next_position.x, next_position.y);
            fprintf(file, "\n(%d, %d)", next_position.x, next_position.y);
            return next_position;
        }
        else if (store[next_x][next_y] == '-') {
            next_position.x = position.x;
            next_position.y = position.y;
            next_position.px = position.px;
            next_position.py = position.py;
            next_position.pd = position.pd;
            next_position.steps = position.steps;
            next_position.progress = position.progress;
            if (position.progress == 2) {
                if (cq[position.x][position.y][next_direction] > cq[position.px][position.py][position.pd]) {
                    cq[position.px][position.py][position.pd] = cq[position.x][position.y][next_direction] * 0.9;
                }
                cq[position.x][position.y][next_direction] = 1;
                next_position.progress = 3;
            }
            return next_position;
        }
        else {
            if (position.progress == 0) {
                next_position.progress = 1;
            }
            else if (position.progress == 1) {
                if (item_checker(store[next_x][next_y], shopping_list, cart) == 1) {
                    iq[position.x][position.y][next_direction] = 1;
                    next_position.progress = 2;
                }
                else {
                    next_position.progress = 1;
                }
            }
            else {
                next_position.progress = 2;
            }

            sq[position.x][position.y][next_direction] = 1;


            if (position.progress == 0) {
                if (sq[position.x][position.y][next_direction] > sq[position.px][position.py][position.pd]) {
                    sq[position.px][position.py][position.pd] = sq[position.x][position.y][next_direction] * 0.9;
                }
            }
            else if (position.progress == 1) {
                if (iq[position.x][position.y][next_direction] > iq[position.px][position.py][position.pd]) {
                    iq[position.px][position.py][position.pd] = iq[position.x][position.y][next_direction] * 0.9;
                }
            }
            else if (position.progress == 2) {
                if (cq[position.x][position.y][next_direction] > cq[position.px][position.py][position.pd]) {
                    cq[position.px][position.py][position.pd] = cq[position.x][position.y][next_direction] * 0.9;
                }
            }

            next_position.x = position.x;
            next_position.y = position.y;
            next_position.px = position.px;
            next_position.py = position.py;
            next_position.pd = position.pd;
            next_position.steps = position.steps;
            return next_position;
        }
    }
    else {
        next_position.x = position.x;
        next_position.y = position.y;
        next_position.px = position.px;
        next_position.py = position.py;
        next_position.pd = position.pd;
        next_position.steps = position.steps;
        next_position.progress = position.progress;
        return next_position;
    }
}


int main(void) {

    srand((unsigned int)time(NULL));
    
    time_t t = time(NULL);
	struct tm *local = localtime(&t);
    char now[50];
    sprintf(now, "./output/%04d-%02d-%02d_%02d-%02d-%02d.txt", local->tm_year + 1900, local->tm_mon + 1, local->tm_mday, local->tm_hour, local->tm_min, local->tm_sec);
    printf("%s\n", now);

    FILE *file;
    file = fopen(now, "w");
    fprintf(file, "df31.c output data\n\n");

    // Fetch data from input files
    int starting_x = 0;
    int starting_y = 0;
    char shopping_list[max_items];
    char store[vertical][horizontal];
    float sq[vertical][horizontal][4];
    float iq[vertical][horizontal][4];
    float cq[vertical][horizontal][4];

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

    char *urls_1[4] = { "./input/q/shelf/q0.txt", "./input/q/shelf/q1.txt", "./input/q/shelf/q2.txt", "./input/q/shelf/q3.txt" };
    char *urls_2[4] = { "./input/q/item/q0.txt", "./input/q/item/q1.txt", "./input/q/item/q2.txt", "./input/q/item/q3.txt" };
    char *urls_3[4] = { "./input/q/checkout/q0.txt", "./input/q/checkout/q1.txt", "./input/q/checkout/q2.txt", "./input/q/checkout/q3.txt" };

    read_q(sq, urls_1); 
    read_q(iq, urls_2); 
    read_q(cq, urls_3); 

    // Alphabed list
    char alphabet[26]; 
    for (int i = 0; i < 26; i++) {
        alphabet[i] = 'A' + i;
    }

    char cart[max_items] = {0};
    
    int keep_going = 1;
    struct Position position;
    position.x = starting_x;
    position.y = starting_y;
    position.d = 0;
    position.steps = 0;
    position.px = starting_x;
    position.py = starting_y;
    position.pd = 0;
    position.progress = 0;
    while(keep_going == 1) {
        position = walk(store, shopping_list, cart, file, sq, iq, cq, position);
        if (position.progress == 3) {
            keep_going = 0;
        }
    }

    // Output my cart
    printf("\n");
    printf("Items: ");
    fprintf(file, "\n\nCart: ");
    for (int i = 0; i < max_items; i++) {
        if (cart[i] != '\0'){
            printf("%c -> ", cart[i]);
            fprintf(file, "%c -> ", cart[i]);
        }
    }
    fprintf(file, "\n");

    // Output your steps
    printf("\n");
    printf("Steps: %d", position.steps);
    fprintf(file, "\nSteps: %d\n\n", position.steps);

    // Output the store map
    printf("\n\n");
    for (int i = 0; i < vertical; i++) {
        for (int j = 0; j < horizontal; j++) {
            printf("%c", store[i][j]);
            fprintf(file, "%c", store[i][j]);
        }
        printf("\n"); 
        fprintf(file, "\n");
    }

    write_q(sq, urls_1); 
    write_q(iq, urls_2); 
    write_q(cq, urls_3); 

    fclose(file);

    return 0;
}