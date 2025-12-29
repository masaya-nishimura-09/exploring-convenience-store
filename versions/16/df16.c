#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>
#define vertical 20
#define horizontal 50


int shopping_list_checker(int n, int shelf_number, int shopping_list[n]) {
    int should_visit = 0;
    for (int i = 0; i < n; i++) {
        if (shelf_number == shopping_list[i]) {
            should_visit = 1;
        }
    }
    return should_visit;
}


int shelf_numbers_checker(int o, int shelf_number, int shelf_visited[o]) {
    int should_visit = 1;
    for (int i = 0; i < o; i++) {
        if (shelf_number == shelf_visited[i]) {
            should_visit = 0;
        }
    }
    if (should_visit == 1) {
        for (int i = 0; i < o; i++) {
            if (shelf_visited[i] == -1) {
                shelf_visited[i] = shelf_number;
                break;
            }
        }
    }
    return should_visit;
}


void search(
    int store[vertical][horizontal], 
    int n, int cart[n][2], 
    int o, int shelf_position[o][4], int shelf_visited[o], 
    int starting_x, int starting_y,
    int step, int shopping_list[n]
    ) {
    
    int next_shelf = 0;
    int last_x;
    int last_y;

    // Right
    for (int i = 0; i <= step; i++) {
        if (starting_x < vertical && 0 <= starting_x && starting_y + i < horizontal && 0 <= starting_y + i){
            if (store[starting_x][starting_y + i] == 0 || store[starting_x][starting_y + i] == 8 || store[starting_x][starting_y + i] == 1) {
                // store[starting_x][starting_y + i] = 8;
            } 
            else {
                if (store[starting_x][starting_y + i] < 8 && store[starting_x][starting_y + i] > 2 
                    && shopping_list_checker(n, store[starting_x][starting_y + i], shopping_list) == 1
                    ){
                    if (shelf_numbers_checker(o, store[starting_x][starting_y + i], shelf_visited) == 1 ) {
                        next_shelf = store[starting_x][starting_y + i];
                        last_x = starting_x;
                        last_y = starting_y + i;
                        break;
                    }
                }
            }     
        }
        last_x = starting_x;
        last_y = starting_y + i;
    }
    starting_x = last_x;
    starting_y = last_y;

    // Down
    if (next_shelf == 0) {
        for (int i = 0; i <= step; i++) {
            if (starting_x + i < vertical && 0 <= starting_x + i && starting_y < horizontal && 0 <= starting_y){
                if (store[starting_x + i][starting_y] == 0 || store[starting_x + i][starting_y] == 8) {
                    // store[starting_x + i][starting_y] = 8;
                } 
                else {
                    if (store[starting_x + i][starting_y] < 8 && store[starting_x + i][starting_y] > 2 
                        && shopping_list_checker(n, store[starting_x + i][starting_y], shopping_list) == 1
                        ){ 
                        if (shelf_numbers_checker(o, store[starting_x + i][starting_y], shelf_visited) == 1 ) {
                            next_shelf = store[starting_x + i][starting_y];
                            last_x = starting_x + i;
                            last_y = starting_y;
                            break;
                        }
                    }
                }     
            }
            last_x = starting_x + i;
            last_y = starting_y;
        }
        starting_x = last_x;
        starting_y = last_y;
    }

    // Left
    if (next_shelf == 0) {
        for (int i = 0; i <= step; i++) {
            if (starting_x < vertical && 0 <= starting_x && starting_y - i < horizontal && 0 <= starting_y - i){
                if (store[starting_x][starting_y - i] == 0 || store[starting_x][starting_y - i] == 8) {
                    // store[starting_x][starting_y - i] = 8;
                } 
                else {
                    if (store[starting_x][starting_y - i] < 8 && store[starting_x][starting_y - i] > 2 
                        && shopping_list_checker(n, store[starting_x][starting_y - i], shopping_list) == 1
                        ){
                        if (shelf_numbers_checker(o, store[starting_x][starting_y - i], shelf_visited) == 1) {
                            next_shelf = store[starting_x][starting_y - i];
                            last_x = starting_x;
                            last_y = starting_y - i;
                            break;
                        }
                    }
                }     
            }
            last_x = starting_x;
            last_y = starting_y - i;
        }
        starting_x = last_x;
        starting_y = last_y;
    }

    // Up
    if (next_shelf == 0) {
        for (int i = 0; i <= step; i++) {
            if (starting_x - i < vertical && 0 <= starting_x - i && starting_y < horizontal && 0 <= starting_y){
                if (store[starting_x - i][starting_y] == 0 || store[starting_x - i][starting_y] == 8) {
                    // store[starting_x - i][starting_y] = 8;
                } 
                else {
                    if (store[starting_x - i][starting_y] < 8 && store[starting_x - i][starting_y] > 2 
                    && shopping_list_checker(n, store[starting_x - i][starting_y], shopping_list) == 1
                    ){
                        if (shelf_numbers_checker(o, store[starting_x - i][starting_y], shelf_visited) == 1 ) {
                            next_shelf = store[starting_x - i][starting_y];
                            last_x = starting_x - i;
                            last_y = starting_y;
                            break;
                        }
                    }
                }     
            }
            last_x = starting_x - i;
            last_y = starting_y;
        }
        starting_x = last_x;
        starting_y = last_y;
    }

    if (next_shelf == 0) {
        search(store, n, cart, o, shelf_position, shelf_visited, starting_x - 1, starting_y - 1, step + 2, shopping_list);
    }
    else if (next_shelf > 2 && next_shelf < 8) {           
        // printf("\n次の棚: %d", next_shelf);
        int finish = 1;
        for (int i = 0; i < n; i++) {
            int match = 0;
            for (int j = 0; j < o; j++) {
                if (shopping_list[i] == shelf_visited[j]) {
                    match = 1;
                }
            }
            if (match == 0) {
                finish = 0;
                break;
            }
        }
        if (finish == 0) {
            step = 2;
            search(store, n, cart, o, shelf_position, shelf_visited, starting_x - 1, starting_y - 1, step, shopping_list);
        }
    }
}


int main(void) {
    int n, store[vertical][horizontal];

    printf("アイテム数を入力: ");
    scanf("%d", &n);

    // Create a shopping list
    int shopping_list[n];
    srand((unsigned int)time(NULL));
    for (int i = 0; i < n; i++) {
        shopping_list[i] = rand() % 5 + 3;
    }

    // Create a shopping cart
    int cart[n][2];
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < 2; j++) {
            cart[i][j] = -1;
        }
    }

    // Create a shelves visited list
    int o = 5;
    int shelf_visited[o];
    for (int i = 0; i < o; i++) {
        shelf_visited[i] = -1;
    }

    // Initialize the store map
    for (int i = 0; i < vertical; i++) {
        for (int j = 0; j < horizontal; j++) {
            store[i][j] = 0;
        }
    }

    // Shelves position
    printf("\n棚の座標\n");
    int shelf_position[o][4];
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
                if (store[s - 1][t - 1] == 1 || store[s - 1][t] == 1 || store[s - 1][t + 1] == 1 || 
                store[s][t - 1] == 1 || store[s][t] == 1 || store[s][t + 1] == 1 || 
                store[s + 1][t - 1] == 1 || store[s + 1][t] == 1 || store[s + 1][t + 1] == 1) {
                    again = 1;
                }
            }
        }
        if (again == 0) {
           for (int s = xs; s < xe + 1; s++) {
                for (int t = ys; t < ye + 1; t++) {
                    store[s][t] = 1;
                }
            }
            printf("%d (%d, %d), (%d, %d)\n", i + 3, xs, ys, xe, ye);
            shelf_position[i][0] = xs;
            shelf_position[i][1] = ys;
            shelf_position[i][2] = xe;
            shelf_position[i][3] = ye;
        }
        else {
            i -=1;
        }
    }

    // Items position
    int category = 3;
    for (int i = 0; i < o; i++) {
        int xs = shelf_position[i][0];
        int ys = shelf_position[i][1];
        int xe = shelf_position[i][2];
        int ye = shelf_position[i][3];
        for (int j = xs; j <= xe; j++) {
            store[j][ys] = category;
        }
        for (int j = ys; j <= ye; j++) {
            store[xs][j] = category;
        }
        for (int j = xs; j <= xe; j++) {
            store[j][ye] = category;
        }
        for (int j = ys; j <= ye; j++) {
            store[xe][j] = category;
        }
        category ++;
    }

    printf("\n買い物リスト\n");
    printf("3:弁当, 4:飲み物, 5:スイーツ, 6:雑貨, 7:その他\n");
    for (int i = 0; i < n; i++) {
        printf("%d, ", shopping_list[i]);
    }
    printf("\n");

    // Starting position
    int again = 1;
    int starting_x;
    int starting_y;
    while(again) {
        starting_x = rand() % vertical;
        starting_y = rand() % horizontal;
        if (store[starting_x][starting_y] == 0) {
            again = 0;
        }
    }
    store[starting_x][starting_y] = 8;
    printf("\n始点:(%d, %d)", starting_x, starting_y);

    // Step
    int step = 2;
    search(store, n, cart, o, shelf_position, shelf_visited, starting_x - 1, starting_y - 1, step, shopping_list);

    // Output the route
    printf("\n");
    printf("経路: ");
    for (int i = 0; i < o; i++) {
        if (shelf_visited[i] > 0) {
            printf("%d -> ", shelf_visited[i]);
        }
    }
    
    // Output the store map
    printf("\n\n0:通過していない点, 1:棚, 2:通過した棚, 3~7:商品, 8:通過点");
    printf("\n");
    for (int i = 0; i < vertical; i++) {
        for (int j = 0; j < horizontal; j++) {
            printf("%d", store[i][j]);
        }
        printf("\n"); 
    }

    return 0;
}
 
