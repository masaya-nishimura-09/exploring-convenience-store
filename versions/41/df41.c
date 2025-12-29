#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>
#define vertical 20
#define horizontal 50
#define max_items 4

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

struct Result {
    int next_direction;
    int q_number;
};

struct QFileGroup {
    int q_number;
    char *paths[4];
};

int is_random_walk() {
    int e = rand() % 10;
    if (e < 2) {
        return 1;
    }
    else {
        return 0;
    }
}

int q_used_checker(char item, char cart[max_items]) {
    for (int i = 0; i < max_items; i++) {
        if (cart[i] == item) {
            return 1;
        }
    }
    return 0;
}

int cart_checker(char item, char cart[max_items]) {
    for (int i = 0; i < max_items; i++) {
        if (cart[i] == item) {
            return 1;
        }
    }
    for (int i = 0; i < max_items; i++) {
        if (cart[i] == '\0') {            
            cart[i] = item;
            return 0;
        }
    }
    return 1;
}

int item_checker(
    char item, 
    char shopping_list[max_items], 
    char cart[max_items]
) {
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
    float q[max_items][vertical][horizontal][4], 
    struct QFileGroup *group
){
    FILE *write_file;

    for (int k = 0; k < 4; k++) {
        write_file = fopen(group->paths[k], "w");

        for (int i = 0; i < vertical; i++) {
            for (int j = 0; j < horizontal; j++) {
                fprintf(write_file, "%f ", q[group->q_number - 1][i][j][k]);
            }
            fprintf(write_file, "\n");
        }
        fclose(write_file); 
    }
}

void read_q(
    float q[max_items][vertical][horizontal][4], 
    struct QFileGroup *group
) {
    FILE *read_file;

    for (int k = 0; k < 4; k++) {
        read_file = fopen(group->paths[k], "r");

        for (int i = 0; i < vertical; i++) {
            for (int j = 0; j < horizontal; j++) {
                fscanf(read_file, "%f", &q[group->q_number - 1][i][j][k]);
            }            
        }
        fclose(read_file); 
    }
}

struct Result q_comparison(
    float iq[max_items][vertical][horizontal][4], 
    int x, 
    int y, 
    int random_direction, 
    int progress, 
    char shopping_list[max_items], 
    char cart[max_items]
) {
    struct Result res;

    res.q_number = max_items - 1;
    res.next_direction = random_direction;
    float value = 0;

    if (progress == max_items - 1) {
        for (int i = 0; i < 4; i++) {
            if (value < iq[max_items - 1][x][y][i]) {
                value = iq[max_items - 1][x][y][i];
                res.next_direction = i;
            }
        }
    }
    else {
        for (int i = 0; i < max_items - 1; i++) {
            int is_q_used = 0;
            char item = shopping_list[i];

            is_q_used = q_used_checker(item, cart);

            if (is_q_used == 0) {
                for (int j = 0; j < 4; j++) {
                    if (value < iq[i][x][y][j]) {
                        value = iq[i][x][y][j];
                        res.next_direction = j;
                        res.q_number = i;
                    }
                }
            }
        }
    }

    if (value == 0) {
        res.next_direction = random_direction;
    }

    return res;
}

struct Position walk(
    char store[vertical][horizontal], 
    char shopping_list[max_items], 
    char cart[max_items], 
    FILE *file, 
    float iq[max_items][vertical][horizontal][4], 
    struct Position position
) {
    struct Position next_position;

    int next_direction = rand() % 4;
    int q_number = max_items - 1;
    int random_walk = is_random_walk();

    if (random_walk == 0) {
        if (position.progress < max_items - 1) {
            // When looking for items
            struct Result r = q_comparison(iq, position.x, position.y, next_direction, position.progress, shopping_list, cart);
            next_direction = r.next_direction;
            q_number = r.q_number;
        }
        else {
            // When looking for the checkout
            float value = 0;
            int direction = 0;

            for (int i = 0; i < 4; i++) {
                if (value < iq[max_items - 1][position.x][position.y][i]) {
                    value = iq[max_items - 1][position.x][position.y][i];
                    direction = i;
                }
            }

            if (value != 0) {
                next_direction = direction;
            }
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

    // If next position is in the map.
    if (next_x >= 0 && next_y >= 0 && next_x < vertical && next_y < horizontal){
        // If next position is empty or the places passed
        if (store[next_x][next_y] == ' ' || store[next_x][next_y] == '*') {
            store[next_x][next_y] = '*';
            next_position.x = next_x;
            next_position.y = next_y;
            next_position.px = position.x;
            next_position.py = position.y;
            next_position.pd = next_direction;
            next_position.steps = position.steps + 1;
            next_position.progress = position.progress;

            for (int i = 0; i < max_items; i++) {
                if (iq[i][position.x][position.y][next_direction] > iq[i][position.px][position.py][position.pd]) {
                    iq[i][position.px][position.py][position.pd] = iq[i][position.x][position.y][next_direction] * 0.9;
                }
            }

            printf("\n(%d, %d)", next_position.x, next_position.y);
            fprintf(file, "\n(%d, %d)", next_position.x, next_position.y);
            return next_position;
        }
        // If next position is on the checkout
        else if (store[next_x][next_y] == '-') {
            next_position.x = position.x;
            next_position.y = position.y;
            next_position.px = position.px;
            next_position.py = position.py;
            next_position.pd = position.pd;
            next_position.steps = position.steps;
            next_position.progress = position.progress;
            if (position.progress == max_items - 1) {
                for (int i = 0; i < max_items; i++) {
                    if (iq[i][position.x][position.y][next_direction] > iq[i][position.px][position.py][position.pd]) {
                        iq[i][position.px][position.py][position.pd] = iq[i][position.x][position.y][next_direction] * 0.9;
                    }
                }
                iq[max_items - 1][position.x][position.y][next_direction] = 1;
                next_position.progress = max_items;
            }
            return next_position;
        }
        // If next position is on a item
        else {
            int should_pick = item_checker(store[next_x][next_y], shopping_list, cart);

            // When looking for items and a item you just found is unpicked
            if (should_pick == 1 && position.progress < max_items - 1) {
                next_position.progress = position.progress + 1;

                int item_number = 0;

                for (int i = 0; i < max_items - 1; i++) {
                    if (store[next_x][next_y] == shopping_list[i]) {
                        item_number = i;
                    }
                }

                iq[item_number][position.x][position.y][next_direction] = 1;
            }
            // When looking for the checkout or a item you just found is already picked
            else {
                next_position.progress = position.progress;
            }
           
            for (int i = 0; i < max_items; i++) {
                if (iq[i][position.x][position.y][next_direction] > iq[i][position.px][position.py][position.pd]) {
                    iq[i][position.px][position.py][position.pd] = iq[i][position.x][position.y][next_direction] * 0.9;
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
    fprintf(file, "df41.c output data\n\n");

    // Fetch data from input files
    int starting_x = 0;
    int starting_y = 0;
    char shopping_list[max_items];
    char store[vertical][horizontal];
    float iq[max_items][vertical][horizontal][4];

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
        int i = 0;
        char ch;
        while (fscanf(shopping_list_file, "%c", &ch) == 1) {
            if ((ch >= 'A' && ch <= 'Z') || ch == '-') {
                shopping_list[i++] = ch;
            }
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

    struct QFileGroup urls_1 = { 1, {
        "./input/q/item1/q0.txt",
        "./input/q/item1/q1.txt",
        "./input/q/item1/q2.txt",
        "./input/q/item1/q3.txt"
    }};

    struct QFileGroup urls_2 = { 2, {
        "./input/q/item2/q0.txt",
        "./input/q/item2/q1.txt",
        "./input/q/item2/q2.txt",
        "./input/q/item2/q3.txt"
    }};

    struct QFileGroup urls_3 = { 3, {
        "./input/q/item3/q0.txt",
        "./input/q/item3/q1.txt",
        "./input/q/item3/q2.txt",
        "./input/q/item3/q3.txt"
    }};

    struct QFileGroup urls_4 = { 4, {
        "./input/q/checkout/q0.txt",
        "./input/q/checkout/q1.txt",
        "./input/q/checkout/q2.txt",
        "./input/q/checkout/q3.txt"
    }};

    read_q(iq, &urls_1); 
    read_q(iq, &urls_2); 
    read_q(iq, &urls_3); 
    read_q(iq, &urls_4); 

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
        position = walk(store, shopping_list, cart, file, iq, position);
        if (position.progress == max_items) {
            keep_going = 0;
        }
    }

    // Output a shopping list
    printf("\n");
    printf("Shopping list: ");
    fprintf(file, "\n\nShopping list: ");
    for (int i = 0; i < max_items; i++) {
        printf("%c -> ", shopping_list[i]);
        fprintf(file, "%c -> ", shopping_list[i]);
    }
    fprintf(file, "\n");

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

    // Output your progress
    printf("\n");
    printf("Progress: %d", position.progress);
    fprintf(file, "\nProgress: %d\n\n", position.progress);

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

    write_q(iq, &urls_1); 
    write_q(iq, &urls_2); 
    write_q(iq, &urls_3); 
    write_q(iq, &urls_4); 


    fclose(file);

    return 0;
}
