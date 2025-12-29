#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>
#define verticle 20
#define horizontal 50

void go_around(int store[vertical][horizontal], int x, int y) {
    int last_x = x;
    int last_y = y;

    // down
    for (x; store[x][y + 1] == 1 || store[x][y + 1] == 2; x++) {
        store[x][y] = 3;
        last_x = x;
    }

    // right
    for (y + 1; store[last_x][y + 1] == 1 || store[last_x][y + 1] == 2; y++) {
        store[last_x + 1][y + 1] = 4;
        int exist = 0;
        int collision = 0;
        for (int j = last_x + 2; j < vertical; j++) {

            if (store[j][y] > 2) {
                break;
            }
            else if (store[j][y] == 1) {
                if (store[j][y - 1] != 1) {
                    exist = 1;
                    collision = j;
                    break;
                }
            }



            // if (store[j][y] != 0) {
            //     if (store[j][y] != 1) {
            //         break;
            //     }
            //     else if (store[j][y] == 1 && store[j - 1][y] == 0) {
            //         exist = 1;
            //         collision = j;
            //         break;
            //     }
            // }




        }
        if (exist == 1) {
            exist = 0;
            for (int j = last_x + 2; j < collision; j++) {
                store[j][y] = 3;
            }
            store[collision -1][y - 1] = 3;
            go_around(store, collision, y - 1);
        }

        last_y = y + 1;
    }
    last_x += 1;

    // up
    for (int i = last_x - 1; store[last_x - 1][last_y] == 1 || store[last_x - 1][last_y] == 2; i--) {
        store[last_x - 1][last_y + 1] = 5;
        last_x = i;
    }
    last_y += 1;
    
    // left
    for (int i = last_y - 1; store[last_x][i] == 1 || store[last_x][i] == 2; i--) {
        store[last_x - 1][i] = 6;
    }
}

void walk(int store[vertical][horizontal]) {
    while(1) {
        for (int i = 0; i < horizontal; i++) {
            store[0][i] = 3;
            int exist = 0;
            int collision = 0;
            for (int j = 1; j < vertical; j++) {
                if (store[j][i] > 2) {
                    break;
                }
                else if (store[j][i] == 1) {
                    if (store[j][i -1] != 1)
                        exist = 1;
                        collision = j;
                        break;
                }



                // if (store[j][i] != 0) {
                //     if (store[j][i] != 1) {
                //         break;
                //     }
                //     else if (store[j][i] == 1 && store[j - 1][i] == 0) {
                //         exist = 1;
                //         collision = j;
                //         break;
                //     }
                // }
            }
            if (exist == 1) {
                exist = 0;
                for (int j = 0; j < collision; j++) {
                    store[j][i] = 3;
                }
                // for (int j = i - 1; store[collision][j] == 0; i--) {
                //     store[collision -1][i - 1] = 3;
                // }
                store[collision -1][i - 1] = 3;
                go_around(store, collision, i -1);
            }
        }
        break;
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

        int xs = rand() % (vertical - 2) + 1;
        int ys = rand() % (horizontal - 2) + 1;
        int xe = rand() % (vertical - 2) + 1;
        int ye = rand() % (horizontal - 2) + 1;

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
                if (store[s][t] == 1) {
                    again = 1;
                }
                // else if (store[s - 1][t - 1] == 1) {
                //     again = 1;
                // }
                // else if (store[s + 1][t + 1] == 1) {
                //     again = 1;
                // }
                // else if (store[s - 1][t + 1] == 1) {
                //     again = 1;
                // }
                // else if (store[s + 1][t - 1] == 1) {
                //     again = 1;
                // }
                // else if (store[s][t - 1] == 1) {
                //     again = 1;
                // }
                // else if (store[s][t + 1] == 1) {
                //     again = 1;
                // }
                // else if (store[s - 1][t] == 1) {
                //     again = 1;
                // }
                // else if (store[s + 1][t] == 1) {
                //     again = 1;
                // }
            }
        }
        if (again == 0) {
           for (int s = xs; s < xe + 1; s++) {
                for (int t = ys; t < ye + 1; t++) {
                    store[s][t] = 1;
                }
            }
            printf("%d, %d, %d, %d\n", xs, ys, xe, ye);
        }
        else {
            i -=1;
        }
    }

    printf("\n");

    v[0][0] = 0;
    v[0][1] = 0;
    for (int i = 1; i < n; i++) {
        int x = rand() % (vertical - 2) + 1;
        int y = rand() % (horizontal - 2) + 1;
        int position = store[x][y];
        if (position == 0) {
            v[i][0] = x;
            v[i][1] = y;
            store[x][y] = 2;
        }
        else {
            i -= 1;
        }
    }
    
    printf("\nアイテム座標\n");
    for (int i = 0; i < n; i++) {
        printf("(%d, %d)", v[i][0], v[i][1]);
        printf("\n");
    }

    walk(store);

    for (int i = 0; i < vertical; i++) {
        for (int j = 0; j < horizontal; j++) {
            printf("%d", store[i][j]);
        }
        printf("\n"); 
    }

    return 0;
}
 