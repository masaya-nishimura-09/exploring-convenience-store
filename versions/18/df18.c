#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>
#define vertical 20
#define horizontal 50


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
};


int finish_checker(int n, char shopping_list[n], char cart[n]) {
    int finish = 1;
    for (int i = 0; i < n; i++) {
        int got = 0;
        for (int j = 0; j < n; j++) {
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

void cart_checker(char item, int n, char cart[n]) {

    for (int i = 0; i < n; i++) {
        if (item == cart[i] || cart[i] == '0') {
            cart[i] = item;
            break;
        }
    }

}

void item_checker(char item, int n, char shopping_list[n], char cart[n]) {
    
    int pick = 0;
    for (int i = 0; i < n; i++) {
        if (item == shopping_list[i]) {
            pick = 1;
        }
    }

    if (pick == 1) {
        cart_checker(item, n, cart);
    }
    
}

struct Position walk(char store[vertical][horizontal], int x, int y, int n, char shopping_list[n], char cart[n], int steps, FILE *file) {

    int next_direction = rand() % 4;
    struct Position position;
    
    if (next_direction == 0) {
        if (x - 1 >= 0 && store[x - 1][y] != ' '){
            if (store[x - 1][y] == '0' || store[x - 1][y] == '1') {
                store[x - 1][y] = '1';
                position.x = x - 1;
                position.y = y;
                position.steps = steps + 1;
                if (position.x - 1 >= 0) {
                    item_checker(store[position.x - 1][position.y], n, shopping_list, cart);
                }
                printf("\n(%d, %d)", position.x, position.y);
                fprintf(file, "\n(%d, %d)", position.x, position.y);
                return position;
            }
            else {
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
                if (position.y + 1 < horizontal) {
                    item_checker(store[position.x][position.y + 1], n, shopping_list, cart);
                }
                printf("\n(%d, %d)", position.x, position.y);
                fprintf(file, "\n(%d, %d)", position.x, position.y);
                return position;
            }
            else {
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
    else if (next_direction == 2) {
        if (x + 1 < vertical && store[x + 1][y] != ' ') {
            if (store[x + 1][y] == '0' || store[x + 1][y] == '1') {
                store[x + 1][y] = '1';
                position.x = x + 1;
                position.y = y;
                position.steps = steps + 1;
                if (position.x + 1 < vertical) {
                    item_checker(store[position.x + 1][position.y], n, shopping_list, cart);
                }
                printf("\n(%d, %d)", position.x, position.y);
                fprintf(file, "\n(%d, %d)", position.x, position.y);
                return position;
            }
            else {
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
                if (position.y - 1 >= 0) {
                    item_checker(store[position.x][position.y - 1], n, shopping_list, cart);
                }
                printf("\n(%d, %d)", position.x, position.y);
                fprintf(file, "\n(%d, %d)", position.x, position.y);
                return position;
            }
            else {
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
    
    time_t t = time(NULL);
	struct tm *local = localtime(&t);
    char now[50];
    sprintf(now, "%04d-%02d-%02d_%02d-%02d-%02d.txt", local->tm_year + 1900, local->tm_mon + 1, local->tm_mday, local->tm_hour, local->tm_min, local->tm_sec);
    printf("%s\n", now);

    FILE *file;
    file = fopen(now, "w");
    fprintf(file, "df18.c output data\n\n");

    // Number of items
    int n;
    printf("アイテム数を入力: ");
    scanf("%d", &n);
    fprintf(file, "Number of items: \n%d\n", n);

    // Alphabed list
    char alphabet[26]; 
    for (int i = 0; i < 26; i++) {
        alphabet[i] = 'A' + i;
    }

    // Shopping list
    char shopping_list[n];
    srand((unsigned int)time(NULL));
    for (int i = 0; i < n; i++) {
        shopping_list[i] = alphabet[rand() % 26];
    }

    // Shopping cart
    char cart[n];
    for (int i = 0; i < n; i++) {
        cart[i] = '0';
    }

    // Shelves visited list
    int o = 5;
    int shelf_visited[o];
    for (int i = 0; i < o; i++) {
        shelf_visited[i] = -1;
    }

    // Store map
    char store[vertical][horizontal];
    for (int i = 0; i < vertical; i++) {
        for (int j = 0; j < horizontal; j++) {
            store[i][j] = '0';
        }
    }

    // Shelves position
    printf("\n棚の座標\n");
    fprintf(file, "\nPositions of shelves:\n");
    int shelf_position[o][4];
    struct Shelf shelf[o];
    for (int i = 0; i < o; i++) {

        int xs = rand() % (vertical - 4) + 2;
        int ys = rand() % (horizontal - 4) + 2;
        int xe = rand() % (vertical - 4) + 2;
        int ye = rand() % (horizontal - 4) + 2;

        if (xs >= xe) {
            int xx = xs;
            xs = xe;
            xe = xx;
        }
        if (ys >= ye) {
            int yy = ys;
            ys = ye;
            ye = yy;
        }      

        int again = 0;
        for (int s = xs; s < xe + 1; s++) {
            for (int t = ys; t < ye + 1; t++) {
                // if (store[s - 1][t - 1] == '1' || store[s - 1][t] == '1' || store[s - 1][t + 1] == '1' || 
                // store[s][t - 1] == '1' || store[s][t] == '1' || store[s][t + 1] == '1' || 
                // store[s + 1][t - 1] == '1' || store[s + 1][t] == '1' || store[s + 1][t + 1] == '1') {
                //     again = 1;
                // }
                // if (store[s - 1][t - 1] == ' ' || store[s - 1][t] == ' ' || store[s - 1][t + 1] == ' ' || 
                // store[s][t - 1] == ' ' || store[s][t] == ' ' || store[s][t + 1] == ' ' || 
                // store[s + 1][t - 1] == ' ' || store[s + 1][t] == ' ' || store[s + 1][t + 1] == ' ') {
                //     again = 1;
                // }
                if (store[s - 1][t - 1] == ' ' || store[s - 1][t] == ' ' || store[s - 1][t + 1] == ' ' || 
                store[s][t - 1] == ' ' || store[s][t] == ' ' || store[s][t + 1] == ' ' || 
                store[s + 1][t - 1] == ' ' || store[s + 1][t] == ' ' || store[s + 1][t + 1] == ' ') {
                    again = 1;
                }
            }
        }
        if (again == 0) {
           for (int s = xs; s < xe + 1; s++) {
                for (int t = ys; t < ye + 1; t++) {
                    store[s][t] = ' ';
                }
            }
            printf("%d: (%d, %d), (%d, %d)\n", i + 1, xs, ys, xe, ye);
            fprintf(file, "%d: (%d, %d), (%d, %d)\n", i + 1, xs, ys, xe, ye);
            shelf_position[i][0] = xs;
            shelf_position[i][1] = ys;
            shelf_position[i][2] = xe;
            shelf_position[i][3] = ye;
            shelf[i].xs = xs;
            shelf[i].ys = ys;
            shelf[i].xe = xe;
            shelf[i].ye = ye;
        }
        else {
            i--;
        }
    }

    // Put items on shelves
    for (int a = 0; a < o; a++) {
        for (int i = shelf_position[a][0]; i <= shelf_position[a][2]; i++) {
            for (int j = shelf_position[a][1]; j <= shelf_position[a][3]; j++) {
                if (i == shelf_position[a][0] || i == shelf_position[a][2] || j == shelf_position[a][1] || j == shelf_position[a][3]) {
                    store[i][j] = alphabet[rand() % 26];;
                }
            }
        }
    }

    printf("\n買い物リスト\n");
    fprintf(file, "\nShopping list:\n");
    for (int i = 0; i < n; i++) {
        printf("%c, ", shopping_list[i]);
        fprintf(file, "%c, ", shopping_list[i]);
    }
    printf("\n");
    fprintf(file, "\n");

    // Starting position
    int again = 1;
    int starting_x = -1;
    int starting_y = -1;
    while(again) {
        starting_x = rand() % vertical;
        starting_y = rand() % horizontal;
        if (store[starting_x][starting_y] == '0') {
            again = 0;
            break;
        }
    }
    store[starting_x][starting_y] = '1';
    printf("\n経路\n(%d, %d)", starting_x, starting_y);
    fprintf(file, "\nRoute: \n(%d, %d)", starting_x, starting_y);
    
    int steps = 0;
    int keep_going = 1;
    struct Position position;
    position.x = starting_x;
    position.y = starting_y;
    position.steps = 0;
    while(keep_going == 1) {
        position = walk(store, position.x, position.y, n, shopping_list, cart, steps, file);
        steps = position.steps;
        if (finish_checker(n, shopping_list, cart) == 1) {
            keep_going = 0;
        }
    }

    // Output my cart
    printf("\n");
    printf("アイテム: ");
    fprintf(file, "\n\nCart:\n");
    for (int i = 0; i < n; i++) {
        printf("%c -> ", cart[i]);
        fprintf(file, "%c -> ", cart[i]);
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

    return 0;
}