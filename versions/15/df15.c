#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>
#define vertical 20
#define horizontal 50


int item_checker(int n, int cart[n][2], int a, int b) {
    int already_picked = 0;
    for (int i = 0; i < n; i++) {
        if (cart[i][0] == a && cart[i][1] == b) {
            already_picked = 1;
        }
    }
    if (already_picked == 0) {
        for (int i = 0; i < n; i++) {
            if (cart[i][0] == -1 && cart[i][1] == -1) {
                cart[i][0] = a;
                cart[i][1] = b;
                break;
            }
        }
    }
    int finish = 0;
    if (cart[n - 1][0] != -1 && cart[n - 1][1] != -1) {
        finish = 1;
    }
    return finish;
}

void shelf_checker(int o, int shelf_xsys[o][2], int shelf_visited[o][2], int a, int b) {
    int already_picked = 0;
    for (int i = 0; i < o; i++) {
        if (shelf_visited[i][0] == a && shelf_visited[i][1] == b) {
            already_picked = 1;
        }
    }
    int is_matched = 0;
    for (int i = 0; i < o; i++) {
        if (shelf_xsys[i][0] == a && shelf_xsys[i][1] == b) {
            is_matched = 1;
        }
    }
    if (already_picked == 0 && is_matched == 1) {
        for (int i = 0; i < o; i++) {
            if (shelf_visited[i][0] == -1 && shelf_visited[i][1] == -1) {
                shelf_visited[i][0] = a;
                shelf_visited[i][1] = b;
                break;
            }
        }
    }
}

int go_around(
    int store[vertical][horizontal], int a, int b, int shelf_order, 
    int n, int cart[n][2], 
    int o, int shelf_xsys[o][2], int shelf_visited[o][2]
    ) {
    
    int last_x = a;
    int last_y = b;
    int finish = 0;

    // down
    int start_x = last_x;
    for (int x = last_x; store[x][last_y] == 1 || store[x][last_y] == 2; x++) {
        if (start_x != x && store[x][last_y] == 2) {
            if (item_checker(n, cart, x, last_y) == 1) {
                finish = 1;
                break;
            };
        }
        store[x][last_y - 1] = 3;
        last_x = x;
    }
    if (finish == 1) {
        return 1;
    }
    store[last_x + 1][last_y - 1] = 3;
    last_x += 1;
    last_y -= 1;
    

    // right
    int start_y = last_y + 1;
    for (int y = last_y + 1; store[last_x - 1][y] == 1 || store[last_x - 1][y] == 2; y++) {
        if (y != start_y && store[last_x - 1][y] == 2) {
            if (item_checker(n, cart, last_x - 1, y) == 1) {
                finish = 1;
                break;
            };
        }
        // store[last_x][y] = 4;
        store[last_x][y] = 3;
        last_y = y;

        int exist = 0;
        int collision = 0;
        for (int i = last_x + 1; i < vertical; i++) {
            if (store[i][y] > 2) {
                break;
            }
            else if (store[i][y] == 1) {
                if (store[i][y - 1] == 0 || store[i][y - 1] == 3) {
                    exist = 1;
                    collision = i;
                    break;
                }
            }
            else if (store[i][y] == 2 && store[i][y - 1] != 1) {
                exist = 2;
                collision = i;
                break;
            }
        }

        if (exist == 1) {
            for (int i = last_x; i < collision; i++) {
                store[i][y -1] = 3;
            }
            shelf_checker(o, shelf_xsys, shelf_visited, collision, y);
            go_around(store, collision, y, exist, n, cart, o, shelf_xsys, shelf_visited);
            exist = 0;
        }
        else if (exist == 2) {
            for (int i = last_x; i < collision; i++) {
                store[i][y -1] = 3;
            }
            if (store[collision + 1][y] == 2) {
                if (item_checker(n, cart, collision + 1, y) == 1) {
                    finish = 1;
                    break;
                };
                shelf_checker(o, shelf_xsys, shelf_visited, collision + 1, y);
            }
            go_around(store, collision, y, exist, n, cart, o, shelf_xsys, shelf_visited);
            exist = 0;
        }
    }
    if (finish == 1) {
        return 1;
    }

    // store[last_x][last_y + 1] = 4;
    store[last_x][last_y + 1] = 3;
    int exist = 0;
    int collision = 0;
    for (int i = last_x + 1; i < vertical; i++) {
        if (store[i][last_y + 1] > 2) {
            break;
        }
        else if (store[i][last_y + 1] == 1 && store[i][last_y] == 0) {
            exist = 1;
            collision = i;
            break;
        }
        else if (store[i][last_y + 1] == 2 && store[i][last_y] != 1) {
            exist = 2;
            collision = i;
            break;
        }
    }
    if (exist == 1) {
        for (int i = last_x; i < collision; i++) {
            store[i][last_y] = 3;
        }
        shelf_checker(o, shelf_xsys, shelf_visited, collision, last_y + 1);
        go_around(store, collision, last_y + 1, exist, n, cart, o, shelf_xsys, shelf_visited);
        exist = 0;
    }
    else if (exist == 2) {
        for (int i = last_x; i < collision; i++) {
            store[i][last_y] = 3;
        }
        if (item_checker(n, cart, collision, last_y + 1) == 1) {
            finish = 1;
        }
        shelf_checker(o, shelf_xsys, shelf_visited, collision, last_y + 1);
        go_around(store, collision, last_y + 1, exist, n, cart, o, shelf_xsys, shelf_visited);
        exist = 0;
    }
    if (finish == 1) {
        return 1;
    }
    last_y += 1;
    

    // up
    start_x = last_x - 1;
    for (int x = last_x - 1; store[x][last_y - 1] == 1 || store[x][last_y - 1] == 2; x--) {
        if (start_x != x && store[x][last_y - 1] == 2) {
            if (item_checker(n, cart, x, last_y - 1) == 1) {
                finish = 1;
                break;
            }
        }
        // store[x][last_y] = 5;
        store[x][last_y] = 3;
        last_x = x - 1;
    }
    if (finish == 1) {
        return 1;
    }
    store[last_x][last_y] = 3;

    
    // left
    start_y = last_y - 1;
    for (int y = last_y - 1; store[last_x + 1][y] == 1 || store[last_x + 1][y] == 2; y--) {
        if (start_y != y && store[last_x + 1][y] == 2) {
            if (item_checker(n, cart, last_x + 1, y) == 1) {
                finish = 1;
                break;
            };
        }
        store[last_x][y] = 3;
    }
    if (finish == 1) {
        return 1;
    }
    return 0;
}

void walk(
    int store[vertical][horizontal], 
    int n, int cart[n][2], 
    int o, int shelf_xsys[o][2], int shelf_visited[o][2]
    ) {

    int shelf_order = 4;
    int finish = 0;
    for (int i = 0; i < horizontal && finish == 0; i++) {
        store[0][i] = 3;
        int exist = 0;
        int collision = 0;
        for (int j = 1; j < vertical; j++) {
            if (store[j][i] > 2) {
                break;
            }
            else if (store[j][i] == 1) {
                exist = 1;
                collision = j;
                break;
            }
            else if (store[j][i] == 2) {
                exist = 2;
                collision = j;
                break;
            }
        }

        if (exist == 1) {
            for (int j = 0; j < collision; j++) {
                store[j][i - 1] = 3;
            }
            shelf_checker(o, shelf_xsys, shelf_visited, collision, i);
            if (go_around(store, collision, i, shelf_order, n, cart, o, shelf_xsys, shelf_visited) == 1) {
                finish = 1;
            }
            exist = 0;
        }
        else if (exist == 2) {
            for (int j = 0; j < collision; j++) {
                store[j][i - 1] = 3;
            }
            if (item_checker(n, cart, collision, i) == 1) {
                break;
            };
            shelf_checker(o, shelf_xsys, shelf_visited, collision, i);
            if (go_around(store, collision, i, shelf_order, n, cart, o, shelf_xsys, shelf_visited) == 1) {
                finish = 1;
            }
            exist = 0;
        }
    }
}

int main(void) {
    int n, o, store[vertical][horizontal];

    printf("アイテム数を入力: ");
    scanf("%d", &n);
    // printf("\n");

    // アイテム配列
    int v[n][2];

    // 買い物かご
    int cart[n][2];
    // 買い物かごの座標全てを初期値-1にする
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < 2; j++) {
            cart[i][j] = -1;
        }
    }

    printf("障害物数を入力: ");
    scanf("%d", &o);
    // printf("\n");

    // 障害物配列
    int shelf_xsys[o][2];
    int shelf_visited[o][2];
    // 訪れた棚座標全てを初期値-1にする
    for (int i = 0; i < o; i++) {
        for (int j = 0; j < 2; j++) {
            shelf_visited[i][j] = -1;
        }
    }

    for (int i = 0; i < vertical; i++) {
        for (int j = 0; j < horizontal; j++) {
            store[i][j] = 0;
        }
    }

    srand((unsigned int)time(NULL));
    printf("\n障害物座標\n");
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
            printf("%d (%d, %d), (%d, %d)\n", i + 1, xs, ys, xe, ye);
            shelf_xsys[i][0] = xs;
            shelf_xsys[i][1] = ys;
        }
        else {
            i -=1;
        }
    }

    for (int i = 0; i < n; i++) {
        int x = rand() % (vertical - 2) + 1;
        int y = rand() % (horizontal - 2) + 1;
        int position = store[x][y];
        int position_top = store[x -1][y];
        int position_bottom = store[x + 1][y];
        int position_right = store[x][y + 1];
        int position_left = store[x][y - 1];

        if (position == 1) {
            if (position_top == 0 || position_bottom == 0 || position_right == 0 || position_left == 0) {
                v[i][0] = x;
                v[i][1] = y;
                store[x][y] = 2;
            }
            else {
                i -= 1;
            }
        }
        else {
            i -= 1;
        }
    }
    
    printf("\nアイテム座標\n");
    for (int i = 0; i < n; i++) {
        printf("%d (%d, %d)", i + 1, v[i][0], v[i][1]);
        printf("\n");
    }

    walk(store, n, cart, o, shelf_xsys, shelf_visited);

    printf("\n");
    printf("訪れた障害物順\n");
    for (int i = 0; i < o; i++) {
        printf("%d(%d, %d)\n", i + 1, shelf_visited[i][0], shelf_visited[i][1]);
    }

    printf("\n");
    printf("アイテム取得順\n");
    for (int i = 0; i < n; i++) {
        printf("%d(%d, %d)\n", i + 1, cart[i][0], cart[i][1]);
    }

    // printf("\n\n1:障害物, 2:アイテム, 3:通過点, 4,5,6...:訪れた障害物の順番(4からスタート)\n");
    printf("\n\n1:障害物, 2:アイテム, 3:通過点\n");


    printf("\n");
    for (int i = 0; i < vertical; i++) {
        for (int j = 0; j < horizontal; j++) {
            printf("%d", store[i][j]);
        }
        printf("\n"); 
    }
    return 0;
}
 
