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

struct Next_Shelf {
    int x;
    int y; 
    int shelf_number;
};

struct Next_Shelf distance_checker(
    int x1, int y1, int n, int o, 
    char shopping_list[n], 
    int shelf_visited[o], 
    int shelf_position[o][4]
    ) {

    struct Next_Shelf ns;

    int next_shelf = 0;
    int next_x = 0;
    int next_y = 0;
    int distance = 10000;
    for (int i = 0; i < o; i++) {
        int visited = 0;
        for (int j = 0; j < o; j++) {
            if (shelf_visited[j] == i + 1) {
                visited = 1;
                break;
            }
        }

        if (visited == 0) {
            if (abs(x1 - shelf_position[i][0]) + abs(y1 - shelf_position[i][1]) < distance) {
                distance = abs(x1 - shelf_position[i][0]) + abs(y1 - shelf_position[i][1]);
                next_shelf = i;
                next_x = shelf_position[i][0];
                next_y = shelf_position[i][1];
            }
            if (abs(x1 - shelf_position[i][0]) + abs(y1 - shelf_position[i][3]) < distance) {
                distance = abs(x1 - shelf_position[i][0]) + abs(y1 - shelf_position[i][3]);
                next_shelf = i;
                next_x = shelf_position[i][0];
                next_y = shelf_position[i][3];
            }
            if (abs(x1 - shelf_position[i][2]) + abs(y1 - shelf_position[i][1]) < distance) {
                distance = abs(x1 - shelf_position[i][2]) + abs(y1 - shelf_position[i][1]);
                next_shelf = i;
                next_x = shelf_position[i][2];
                next_y = shelf_position[i][1]; 
            }
            if (abs(x1 - shelf_position[i][2]) + abs(y1 - shelf_position[i][3]) < distance) {
                distance = abs(x1 - shelf_position[i][2]) + abs(y1 - shelf_position[i][3]);
                next_shelf = i;
                next_x = shelf_position[i][2];
                next_y = shelf_position[i][3];
            }
        }
    }

    ns.x = next_x;
    ns.y = next_y;
    ns.shelf_number = next_shelf;
    for (int i = 0; i < o; i++) {
        if (shelf_visited[i] == -1) {
            shelf_visited[i] = next_shelf + 1;
            break;
        }
    }

    return ns;
}

int finish_checker(
    int n, 
    char shopping_list[n], 
    char cart[n]
    ) {
    
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

void get_item(int n, char cart[n], char item) {
    for (int i = 0; i < n; i++ ) {
        if (cart[i] == '0' || cart[i] == item) {
            cart[i] = item;
            break;
        }
    }
}

int item_checker(
    char store[vertical][horizontal], 
    int shelf_number, 
    int n, 
    char shopping_list[n], 
    char cart[n], 
    int o, 
    struct Shelf shelf[o]
    ) {

    for (int i = shelf[shelf_number].xs; i <= shelf[shelf_number].xe; i++) {

        for (int j = shelf[shelf_number].ys; j <= shelf[shelf_number].ye; j++) {
            
            if(i == shelf[shelf_number].xs || i == shelf[shelf_number].xe || j == shelf[shelf_number].ys || j == shelf[shelf_number].ye) {
                for (int item = 0; item < n; item++) {
                    if(store[i][j] == shopping_list[item]) {
                        get_item(n, cart, store[i][j]);
                    }
                }
            }
        }
    }

    return finish_checker(n, shopping_list, cart);
}


int main(void) {

    // Number of items
    int n;
    printf("アイテム数を入力: ");
    scanf("%d", &n);

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
                if (store[s - 1][t - 1] == '1' || store[s - 1][t] == '1' || store[s - 1][t + 1] == '1' || 
                store[s][t - 1] == '1' || store[s][t] == '1' || store[s][t + 1] == '1' || 
                store[s + 1][t - 1] == '1' || store[s + 1][t] == '1' || store[s + 1][t + 1] == '1') {
                    again = 1;
                }
            }
        }
        if (again == 0) {
           for (int s = xs; s < xe + 1; s++) {
                for (int t = ys; t < ye + 1; t++) {
                    store[s][t] = '1';
                }
            }
            printf("%d: (%d, %d), (%d, %d)\n", i + 1, xs, ys, xe, ye);
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
    for (int i = 0; i < n; i++) {
        printf("%c, ", shopping_list[i]);
    }
    printf("\n");

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
    store[starting_x][starting_y] = '2';
    printf("\n始点 2:(%d, %d)", starting_x, starting_y);

    for (int i = 0; i < o; i++) {
        struct Next_Shelf ns = distance_checker(starting_x, starting_y, n, o, shopping_list, shelf_visited, shelf_position);
        starting_x = ns.x;
        starting_y = ns.y;
        if (item_checker(store, ns.shelf_number, n, shopping_list, cart, o, shelf) == 1) {
            break;
        }
    }

    // Output the route
    printf("\n");
    printf("経路: ");
    for (int i = 0; i < o; i++) {
        if (shelf_visited[i] != -1) {
            printf("%d -> ", shelf_visited[i]);
        }
    }

    // Output my cart
    printf("\n");
    printf("アイテム: ");
    for (int i = 0; i < n; i++) {
        printf("%c -> ", cart[i]);
    }

    // Output the store map
    printf("\n\n");
    for (int i = 0; i < vertical; i++) {
        for (int j = 0; j < horizontal; j++) {
            printf("%c", store[i][j]);
        }
        printf("\n"); 
    }

    return 0;
}