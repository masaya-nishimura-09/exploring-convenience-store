#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>
#define vertical 20
#define horizontal 50
#define max_items 1


struct Shelf {
    int xs;
    int ys; 
    int xe;
    int ye;
};

struct Position {
    int x;
    int y; 
    int steps;
    int px;
    int py;
    int pd;
};

// Select if you walk randomly or use a Q
int q_random() {
    int n = rand() % 10;
    if (n < 3) {
        return 0;
    }
    else {
        return 1;
    }
}


int finish_checker(char shopping_list[max_items], char cart[max_items]) {
    int finish = 1;
    for (int i = 0; i < max_items; i++) {
        int got = 0;
        for (int j = 0; j < max_items; j++) {
            if (shopping_list[i] == cart[j]) {
                got = 1;
                break;
            }
        }
        if (got == 0) {
            finish = 0;
            break;
        }
    }

    return finish;
}

void cart_checker(char item, char cart[max_items]) {

    for (int i = 0; i < max_items; i++) {
        if (item == cart[i] || cart[i] == '0') {
            cart[i] = item;
            break;
        }
    }

}

void item_checker(char item, char shopping_list[max_items], char cart[max_items]) {
    
    int pick = 0;
    for (int i = 0; i < max_items; i++) {
        if (item == shopping_list[i]) {
            pick = 1;
        }
    }

    if (pick == 1) {
        cart_checker(item, cart);
    }
    
}

struct Position walk(char store[vertical][horizontal], int x, int y, char shopping_list[max_items], char cart[max_items], int steps, FILE *file, float q[vertical][horizontal][4], int px, int py, int pd) {
    int next_direction = rand() % 4;
    struct Position position;

    
    if (q_random() == 0) {
        int value = 0;
        int q_number = 0;
        for (int i = 0; i < 4; i++) {
            if (value < q[x][y][i]) {
                value = q[x][y][i];
                q_number = i;
            }
        }
        if (value != 0) {
            next_direction = q_number;
        }
    }

    if (next_direction == 0) {
        if (x - 1 >= 0 && store[x - 1][y] != ' '){
            if (store[x - 1][y] == '0' || store[x - 1][y] == '1') {
                store[x - 1][y] = '1';
                position.x = x - 1;
                position.y = y;
                position.steps = steps + 1;
                position.px = x;
                position.py = y;
                position.pd = 0;
                // if (position.x - 1 >= 0) {
                //     item_checker(store[position.x - 1][position.y], shopping_list, cart);
                // }
                // printf("\n(%d, %d)", position.x, position.y);
                if (q[x][y][0] > q[px][py][pd]) {
                    q[px][py][pd] = q[x][y][0] * 0.9;
                }
                printf("\n(%d, %d) Q[%d][%d][%d] %f", position.x, position.y, x, y, 0, q[x][y][0]);
                fprintf(file, "\n(%d, %d)", position.x, position.y);
                return position;
            }
            else {
                item_checker(store[x - 1][y], shopping_list, cart);
                position.x = x;
                position.y = y;
                position.steps = steps;
                return position;
            }
        }
        else {
            position.x = x;
            position.y = y;
            position.steps = steps;
            return position;
        }
    }

    else if (next_direction == 1) {
        if (y + 1 < horizontal && store[x][y + 1] != ' ') {
            if (store[x][y + 1] == '0' || store[x][y + 1] == '1') {
                store[x][y + 1] = '1';
                position.x = x;
                position.y = y + 1;
                position.steps = steps + 1;
                position.px = x;
                position.py = y;
                position.pd = 1;
                // if (position.y + 1 < horizontal) {
                //     item_checker(store[position.x][position.y + 1], shopping_list, cart);
                // }
                // printf("\n(%d, %d)", position.x, position.y);
                if (q[x][y][1] > q[px][py][pd]) {
                    q[px][py][pd] = q[x][y][1] * 0.9;
                }
                printf("\n(%d, %d) Q[%d][%d][%d] %f", position.x, position.y, x, y, 1, q[x][y][1]);
                fprintf(file, "\n(%d, %d)", position.x, position.y);
                return position;
            }
            else {
                item_checker(store[x][y + 1], shopping_list, cart);
                position.x = x;
                position.y = y;
                position.steps = steps;
                return position;            // q[position.x][position.y][2] = 1;
            // q[5][21][2] = 0.8;
            // q[6][22][3] = 0.8;
            // q[7][21][0] = 0.8;
            // q[6][20][1] = 0.8;
            }
        }
        else {
            position.x = x;
            position.y = y;
            position.steps = steps;
            return position;
        }
    }
    else if (next_direction == 2) {
        if (x + 1 < vertical && store[x + 1][y] != ' ') {
            if (store[x + 1][y] == '0' || store[x + 1][y] == '1') {
                store[x + 1][y] = '1';
                position.x = x + 1;
                position.y = y;
                position.steps = steps + 1;
                position.px = x;
                position.py = y;
                position.pd = 2;
                // if (position.x + 1 < vertical) {
                //     item_checker(store[position.x + 1][position.y], shopping_list, cart);
                // }
                // printf("\n(%d, %d)", position.x, position.y);
                if (q[x][y][2] > q[px][py][pd]) {
                    q[px][py][pd] = q[x][y][2] * 0.9;
                }
                printf("\n(%d, %d) Q[%d][%d][%d] %f", position.x, position.y, x, y, 2, q[x][y][2]);
                fprintf(file, "\n(%d, %d)", position.x, position.y);
                return position;
            }
            else {
                item_checker(store[x + 1][y], shopping_list, cart);
                // printf("\n(%d, %d) %f", x + 1, y, q[x][y][2]);
                position.x = x;
                position.y = y;
                position.steps = steps;
                return position;
            }
        }
        else {
            position.x = x;
            position.y = y;
            position.steps = steps;
            return position;
        }
    }
    else {
        if (y - 1 >= 0 && store[x][y - 1] != ' ') {
            if (store[x][y - 1] == '0' || store[x][y - 1] == '1') {
                store[x][y - 1] = '1';
                position.x = x;
                position.y = y - 1;
                position.steps = steps + 1;
                position.px = x;
                position.py = y;
                position.pd = 3;
                // if (position.y - 1 >= 0) {
                //     item_checker(store[position.x][position.y - 1], shopping_list, cart);
                // }
                // printf("\n(%d, %d)", position.x, position.y);
                if (q[x][y][3] > q[px][py][pd]) {
                    q[px][py][pd] = q[x][y][3] * 0.9;
                }
                printf("\n(%d, %d) Q[%d][%d][%d] %f", position.x, position.y, x, y, 3, q[x][y][3]);
                fprintf(file, "\n(%d, %d)", position.x, position.y);
                return position;
            }            // q[position.x][position.y][2] = 1;
            // q[5][21][2] = 0.8;
            // q[6][22][3] = 0.8;
            // q[7][21][0] = 0.8;
            // q[6][20][1] = 0.8;
            else {
                item_checker(store[x][y - 1], shopping_list, cart);
                position.x = x;
                position.y = y;
                position.steps = steps;
                return position;
            }
        }
        else {
            position.x = x;
            position.y = y;
            position.steps = steps;
            return position;
        }
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
    fprintf(file, "df19.c output data\n\n");


    // Fetch data from input files
    int starting_x = 0;
    int starting_y = 0;
    char shopping_list[max_items];
    char store[vertical][horizontal];
    float q[vertical][horizontal][4];

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
    fclose(shopping_list_file);             // q[position.x][position.y][2] = 1;
            // q[5][21][2] = 0.8;
            // q[6][22][3] = 0.8;
            // q[7][21][0] = 0.8;
            // q[6][20][1] = 0.8;

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

    FILE *q0_file;
    FILE *q1_file;
    FILE *q2_file;
    FILE *q3_file;

    if ((q0_file = fopen("./input/q0.txt", "r")) == NULL) {
        printf("Can't open q0.txt.");
    }
    else {
        for (int i = 0; i < vertical; i++) {
            for (int j = 0; j < horizontal; j++) {
                fscanf(q0_file, "%f", &q[i][j][0]);
            }            
        }
    }
    fclose(q0_file); 

    if ((q1_file = fopen("./input/q1.txt", "r")) == NULL) {
        printf("Can't open q1.txt.");
    }
    else {
        for (int i = 0; i < vertical; i++) {
            for (int j = 0; j < horizontal; j++) {
                fscanf(q1_file, "%f", &q[i][j][1]);
            }  
        }
    }
    fclose(q1_file); 

    if ((q2_file = fopen("./input/q2.txt", "r")) == NULL) {
        printf("Can't open q2.txt.");
    }
    else {
        for (int i = 0; i < vertical; i++) {
            for (int j = 0; j < horizontal; j++) {
                fscanf(q2_file, "%f", &q[i][j][2]);
            }  
        }
    }
    fclose(q2_file); 

    if ((q3_file = fopen("./input/q3.txt", "r")) == NULL) {
        printf("Can't open q3.txt.");
    }
    else {
        for (int i = 0; i < vertical; i++) {
             for (int j = 0; j < horizontal; j++) {
                fscanf(q3_file, "%f", &q[i][j][3]);
            }  
        }
    }
    fclose(q3_file); 
  

    // Q[20][50][4]
    // int q[vertical][horizontal][4];
    // for (int i = 0; i < vertical; i++) {
    //     for (int j = 0; j < horizontal; j++) {
    //         for (int k = 0; k < 4; k++) {
    //             q[i][j][k] = 0;
    //         }
    //     }
    // }

    // Alphabed list
    char alphabet[26]; 
    for (int i = 0; i < 26; i++) {
        alphabet[i] = 'A' + i;
    }

    // Shopping cart
    char cart[max_items];
    for (int i = 0; i < max_items; i++) {
        cart[i] = '0';
    }
    
    int steps = 0;
    int keep_going = 1;
    struct Position position;
    position.x = starting_x;
    position.y = starting_y;
    position.steps = 0;
    position.px = starting_x;
    position.py = starting_y;
    position.pd = 0;
    // int count = 100;
    while(keep_going == 1) {
        position = walk(store, position.x, position.y, shopping_list, cart, steps, file, q, position.px, position.py, position.pd);
        steps = position.steps;
        // if (count == steps) {
        //     break;
        // }
        if (finish_checker(shopping_list, cart) == 1) {
            keep_going = 0;
            // q[5][21][2] = 1;
            // q[4][21][2] = 0.99;
            // q[5][22][3] = 0.99;
            // q[5][20][1] = 0.99;

        }
    }

    // Output my cart
    printf("\n");
    printf("アイテム: ");
    fprintf(file, "\n\nCart:\n");
    for (int i = 0; i < max_items; i++) {
        if (cart[i]){
            printf("%c -> ", cart[i]);
            fprintf(file, "%c -> ", cart[i]);
        }
    }
    fprintf(file, "\n");

    // Output your steps
    printf("\n");
    printf("歩数: %d", steps);
    fprintf(file, "\nSteps: \n%d\n\n", steps);

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

    fclose(file);



    FILE *q0_output;
    q0_output = fopen("./input/q0.txt", "w");
    for (int i = 0; i < vertical; i++) {
        for (int j = 0; j < horizontal; j++) {
            fprintf(q0_output, "%f ", q[i][j][0]);
        }
        fprintf(q0_output, "\n");
    }
    
    FILE *q1_output;
    q1_output = fopen("./input/q1.txt", "w");
    for (int i = 0; i < vertical; i++) {
        for (int j = 0; j < horizontal; j++) {
            fprintf(q1_output, "%f ", q[i][j][1]);
        }
        fprintf(q1_output, "\n");
    }

    FILE *q2_output;
    q2_output = fopen("./input/q2.txt", "w");
    for (int i = 0; i < vertical; i++) {
        for (int j = 0; j < horizontal; j++) {
            fprintf(q2_output, "%f ", q[i][j][2]);
        }
        fprintf(q2_output, "\n");
    }

    FILE *q3_output;
    q3_output = fopen("./input/q3.txt", "w");
    for (int i = 0; i < vertical; i++) {
        for (int j = 0; j < horizontal; j++) {
            fprintf(q3_output, "%f ", q[i][j][3]);
        }
        fprintf(q3_output, "\n");
    }


    return 0;
}