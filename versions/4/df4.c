#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

// 2点間の距離を計算する
double dist(int x1, int y1, int x2, int y2) {
    return sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1));
}

// 線分の交差判定
int cross(int xa, int ya, int xb, int yb, int xc, int yc, int xd, int yd) {
    double s1, t1, s2, t2;

    s1 = (xa - xb) * (yc - ya) - (ya - yb) * (xc - xa);
    t1 = (xa - xb) * (yd - ya) - (ya - yb) * (xd - xa);

    s2 = (xc - xd) * (ya - yc) - (yc - yd) * (xa - xc);
    t2 = (xc - xd) * (yb - yc) - (yc - yd) * (xb - xc);

    return (s1 * t1 <= 0 && s2 * t2 <= 0);
}

void dfs(int v, int n, int dfnum[], int vv[][2], int count, int o, int ss[][2], int ee[][2], int matrix[n][n]) {
    printf("v%dを訪問\n", v + 1);
    dfnum[v] = 1;
    count++;
    double shortest = 1e9;
    int next = 0;

    for (int i = 0; i < n; i++) {
        if (dfnum[i] == 1 || v == i) continue;

        double distance = dist(vv[v][0], vv[v][1], vv[i][0], vv[i][1]);
        int blocked = 0;
        
        for (int j = 0; j < o; j++) {
            if (cross(vv[v][0], vv[v][1], vv[i][0], vv[i][1], ss[j][0], ss[j][1], ss[j][0], ee[j][1])) {
                blocked = 1;
                break;
            }
            if (cross(vv[v][0], vv[v][1], vv[i][0], vv[i][1], ss[j][0], ee[j][1], ee[j][0], ee[j][1])) {
                blocked = 1;
                break;
            }
            if (cross(vv[v][0], vv[v][1], vv[i][0], vv[i][1], ee[j][0], ee[j][1], ee[j][0], ss[j][1])) {
                blocked = 1;
                break;
            }
            if (cross(vv[v][0], vv[v][1], vv[i][0], vv[i][1], ee[j][0], ss[j][1], ss[j][0], ss[j][1])) {
                blocked = 1;
                break;
            }
        }

        if (!blocked && distance < shortest && matrix[v][i]) {
            shortest = distance;
            next = i;
        }
    }

    if (next == 0) {
        printf("v1に戻る\n");
    } else {
        dfs(next, n, dfnum, vv, count, o, ss, ee, matrix);
    }
}

int main(void) {
    int n, o, count = 0;
    printf("頂点数を入力: ");
    scanf("%d", &n);
    printf("\n障害物数を入力: ");
    scanf("%d", &o);
    printf("\n");

    int vv[n][2];
    int ss[o][2], ee[o][2];
    int matrix[n][n];
    int dfnum[n];

    srand((unsigned int)time(NULL));
    printf("頂点座標\n");
    for (int i = 0; i < n; i++) {
        vv[i][0] = rand() % 100 + 1;
        vv[i][1] = rand() % 100 + 1;
        printf("v%d(%d, %d)\n", i + 1, vv[i][0], vv[i][1]);
    }

    printf("\n隣接行列\n");
    for (int i = 0; i < n; i++)
    {
        for (int j = 0; j < n; j++)
        {
            matrix[i][j] = rand() % 2;
            printf("%d", matrix[i][j]);
        }
        printf("\n");
    }

    printf("\n障害物座標\n");
    for (int i = 0; i < o; i++) {
        ss[i][0] = rand() % 100 + 1;
        ss[i][1] = rand() % 100 + 1;
        ee[i][0] = rand() % 100 + 1;
        ee[i][1] = rand() % 100 + 1;
        printf("(xs, ys) = (%d, %d), (xe, ye) = (%d, %d)\n", ss[i][0], ss[i][1], ee[i][0], ee[i][1]);
    }
    printf("\n");

    for (int i = 0; i < n; i++) {
        dfnum[i] = 0; 
    }

    dfs(0, n, dfnum, vv, count, o, ss, ee, matrix);

    return 0;
}
