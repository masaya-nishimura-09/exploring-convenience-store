#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>
#define verticle 20
#define horizontal 50

// void check_items(int v[][], int x, int y) {
//     for (int i = 0; v[][]; i + 1) {
        
//     }
// }

void go_around(int store[vertical][horizontal], int a, int b) {
    int last_x = a;
    int last_y = b;

    // down
    for (int x = last_x; store[x][last_y] == 1; x++) {
        store[x][last_y - 1] = 3;
        last_x = x;
    }
    store[last_x + 1][last_y - 1] = 3;
    last_x += 1;
    last_y -= 1;

    // right
    for (int y = last_y + 1; store[last_x - 1][y] == 1; y++) {
        store[last_x][y] = 4;
        last_y = y;

        int exist = 0;
        int collision = 0;
        for (int i = last_x + 1; i < vertical; i++) {
            if (store[i][y] > 2) {
                break;
            }
            else if (store[i][y] == 1 && store[i][y - 1] == 0) {
                exist = 1;
                collision = i;
                break;
            }
            else if (store[i][y] == 2 && store[i][y - 1] == 0) {
                exist = 1;
                collision = i;
                break;
            }
            // else if (store[i][y] == 1) {
            //     exist = 1;
            //     collision = i;
            //     break;
            // }
            // else if (store[i][y] == 2) {
            //     exist = 1;
            //     collision = i;
            //     break;
            // }
        }
        if (exist == 1) {
            exist = 0;
            for (int i = last_x; i < collision; i++) {
                store[i][y -1] = 3;
            }
            go_around(store, collision, y);
        }

    }
    store[last_x][last_y + 1] = 4;
    last_y += 1;


    // // right
    // for (y + 1; store[last_x][y + 1] == 1 || store[last_x][y + 1] == 2; y++) {
    //     store[last_x + 1][y + 1] = 4;

    //     int exist = 0;
    //     int collision = 0;
    //     for (int j = last_x + 2; j < verticle; j++) {
    //         if (store[j][y] > 2) {
    //             break;
    //         }
    //         else if (store[j][y] == 1) {
    //             if (store[j][y - 1] != 1) {
    //                 exist = 1;
    //                 collision = j;
    //                 break;
    //             }
    //         }
    //     }
    //     if (exist == 1) {
    //         exist = 0;
    //         for (int j = last_x + 2; j < collision; j++) {
    //             store[j][y] = 3;
    //         }
    //         store[collision -1][y - 1] = 3;
    //         go_around(store, collision, y - 1);
    //     }
    //     last_y = y + 1;
    // }
    // last_x += 1;

    // up
    for (int x = last_x - 1; store[x][last_y - 1] == 1; x--) {
        store[x][last_y] = 5;
        last_x = x - 1;
    }
    store[last_x][last_y] = 5;

    
    // left
    for (int y = last_y - 1; store[last_x + 1][y] == 1; y--) {
        store[last_x][y] = 6;
    }
}

void walk(int store[vertical][horizontal]) {
    for (int i = 0; i < horizontal; i++) {
        store[0][i] = 3;
        int exist = 0;
        int collision = 0;
        for (int j = 1; j < vertical; j++) {
            if (store[j][i] > 2) {
                break;
            }
            // else if (store[j][i] == 1 && store[j][i - 1] == 0) {
            //     exist = 1;
            //     collision = j;
            //     break;
            // }
            // else if (store[j][i] == 2 && store[j][i - 1] == 0) {
            //     exist = 1;
            //     collision = j;
            //     break;
            // }
            else if (store[j][i] == 1) {
                exist = 1;
                collision = j;
                break;
            }
            else if (store[j][i] == 2) {
                exist = 1;
                collision = j;
                break;
            }
        }
        if (exist == 1) {
            exist = 0;
            for (int j = 0; j < collision; j++) {
                store[j][i - 1] = 3;
            }
            go_around(store, collision, i);
        }
    }
}

int main(void) {
    int n, o, store[vertical][horizontal];

    printf("\nアイテム数を入力: ");
    scanf("%d", &n);
    printf("\n");

    int v[n][2];

    printf("\n障害物数を入力: ");
    scanf("%d", &o);
    printf("\n");

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
        }
        else {
            i -=1;
        }
    }

    printf("\n");

    for (int i = 0; i < n; i++) {
        int x = rand() % (vertical - 2) + 1;
        int y = rand() % (horizontal - 2) + 1;
        int position = store[x][y];
        if (position == 0) {
            v[i][0] = x;
            v[i][1] = y;
            // store[x][y] = 2;
            store[x][y] = 1;
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
    printf("\n");

    walk(store);

    for (int i = 0; i < vertical; i++) {
        for (int j = 0; j < horizontal; j++) {
            printf("%d", store[i][j]);
        }
        printf("\n"); 
    }

    return 0;
}
 