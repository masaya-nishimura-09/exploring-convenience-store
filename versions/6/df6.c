// １，全ての障害物を一周する。
// ２，途中でアイテムを見つけると訪れて、戻る。
// ３，

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>


double dist(int x1, int y1, int x2, int y2) {
    return sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1));
}

void dfs(int dfnum[], int qx, int qy, int o, int p1[][2], int p2[][2], int p3[][2], int p4[][2]) {
    double shortest = 1e9;
    int next = 0;
    int point = 0;
    int last_point[o][2];

    for (int i = 0; i < o; i++) {
        if (dist(qx, qy, p1[i][0], p1[i][1]) < shortest && dfnum[i] == 0) {
            shortest = dist(qx, qy, p1[i][0], p1[i][1]);
            next = i;
            point = 1;
        }
        if (dist(qx, qy, p2[i][0], p2[i][1]) < shortest && dfnum[i] == 0) {
            shortest = dist(qx, qy, p2[i][0], p2[i][1]);
            next = i;
            point = 2;
        }
        if (dist(qx, qy, p3[i][0], p3[i][1]) < shortest && dfnum[i] == 0) {
            shortest = dist(qx, qy, p3[i][0], p3[i][1]);
            next = i;
            point = 3;
        }
        if (dist(qx, qy, p4[i][0], p4[i][1]) < shortest && dfnum[i] == 0) {
            shortest = dist(qx, qy, p4[i][0], p4[i][1]);
            next = i;
            point = 4;
        }
    }

    if (point == 1)
    {
        printf("P1 (%d, %d)を訪問\n", p1[next][0], p1[next][1]);
        dfnum[next] = 1;
        dfs(dfnum, p1[next][0], p1[next][1], o, p1, p2, p3, p4);
    }
    else if (point == 2)
    {
        printf("P2 (%d, %d)を訪問\n", p2[next][0], p2[next][1]);
        dfnum[next] = 1;
        dfs(dfnum, p1[next][0], p1[next][1], o, p1, p2, p3, p4);
    }
    else if (point == 3)
    {
        printf("P3 (%d, %d)を訪問\n", p3[next][0], p3[next][1]);
        dfnum[next] = 1;
        dfs(dfnum, p1[next][0], p1[next][1], o, p1, p2, p3, p4);
    }
    else if (point == 4)
    {
        printf("P4 (%d, %d)を訪問\n", p4[next][0], p4[next][1]);
        dfnum[next] = 1;
        dfs(dfnum, p1[next][0], p1[next][1], o, p1, p2, p3, p4);
    }
    else
    {
        printf("終了\n");
    }
}


int main(void) {
    int n, o, count = 0;
    printf("\n障害物数を入力: ");
    scanf("%d", &o);
    printf("\n");

    int p1[o][2], p2[o][2], p3[o][2], p4[o][2];
    int dfnum[o];

    srand((unsigned int)time(NULL));
    printf("\n障害物座標\n");
    // v2→v3
    // ↑　　↓
    // v1←v4
    for (int i = 0; i < o; i++) {

        int n = rand() % 100 + 1;
        int m = rand() % 100 + 1;
        if (n <= m) {
            p1[i][0] = n;
            p2[i][0] = n;
            p3[i][0] = m;
            p4[i][0] = m;
        }
        else {
            p1[i][0] = m;
            p2[i][0] = m;
            p3[i][0] = n;
            p4[i][0] = n;
        }

        n = rand() % 100 + 1;
        m = rand() % 100 + 1;
        if (n <= m) {
            p1[i][1] = n;
            p2[i][1] = m;
            p3[i][1] = m;
            p4[i][1] = n;
        }
        else {
            p1[i][1] = m;
            p2[i][1] = n;
            p3[i][1] = n;
            p4[i][1] = m;
        }
        printf("p1, p2, p3, p4 = (%d, %d), (%d, %d), (%d, %d), (%d, %d)\n", p1[i][0], p1[i][1], p2[i][0], p2[i][1], p3[i][0], p3[i][1], p4[i][0], p4[i][1]);
    }
    printf("\n");

    for (int i = 0; i < o; i++) {
        dfnum[i] = 0; 
    }

    dfs(dfnum, 0, 0, o, p1, p2, p3, p4);

    return 0;
}
