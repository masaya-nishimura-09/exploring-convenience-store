#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>


int main(void) {
    int n, o, store[100][100], v[n][2];

    printf("\nアイテム数を入力: ");
    scanf("%d", &n);
    printf("\n");

    printf("\n障害物数を入力: ");
    scanf("%d", &o);
    printf("\n");

    for (int i = 0; i < 100; i++) {
        for (int j = 0; j < 100; j++) {
            store[i][j] = 0;
        }
    }

    srand((unsigned int)time(NULL));
    printf("\n障害物座標\n");
    for (int i = 0; i < o; i++) {

        int xs = rand() % 100 + 1;
        int ys = rand() % 100 + 1;
        int xe = rand() % 100 + 1;
        int ye = rand() % 100 + 1;
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
        printf("%d, %d, %d, %d\n", xs, ys, xe, ye);

        for (int s = xs; s < xe + 1; s++) {
            for (int t = ys; t < ye + 1; t++) {
                store[s][t] = 1;
            }
        }
    }
    printf("\n");

    for (int i = 0; i < n; i++) {
        int x = rand() % 100 + 1;
        int y = rand() % 100 + 1;
        int position = store[x][y];
        if (position == 0) {
            // v[i][0] = x;
            // v[i][1] = y;
            store[x][y] = 2;
        }
        else {
            i -= 1;
        }
    }
    v[0][0] = 0;
    v[0][1] = 0;
    printf("\nアイテム座標\n");
    for (int i = 0; i < n; i++) {
        printf("(%d, %d)", v[i][0], v[i][1]);
        printf("\n");
    }   


    for (int i = 0; i < 100; i++) {
        for (int j = 0; j < 100; j++) {
            printf("%d", store[i][j]);
        }
        printf("\n"); 
    }

    return 0;
}
 