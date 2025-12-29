#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>


// 2点間の距離を求める
double dist(int x1, int y1, int x2, int y2)
{
    return (sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1)));
}

// 距離が一番近い点を探す
void dfs(int v, int n, int dfnum[], int vv[][2], int count)
{
    printf("v%dを訪問\n", v + 1);
    dfnum[v] = 1;
    count++;
    double shortest = 1e9;
    int next = 0;
    for (int i = 0; i < n; i++)
    {
        double distance = dist(vv[v][0], vv[v][1], vv[i][0], vv[i][1]);
        // printf("%f", distance);
        if (distance != 0 && shortest > distance && dfnum[i] == 0)
        {
            shortest = distance;
            next = i;
        }
    }
    if (count == n)
    {
        printf("v1に戻る\n");
    }
    else
    {
        dfs(next, n, dfnum, vv, count);
    }
        
}

// 隣接点を探す
void dfs(int v, int n, int matrix[n][n], int dfnum[])
{
    printf("v%dを訪問。\n", v + 1);
    dfnum[v] = 1; 

    for (int i = 0; i < n; i++)
    {
        if (matrix[v][i] == 1 && dfnum[i] == 0)
        { 
            dfs(i, n, matrix, dfnum);
        }
    }
}

int cross(int xsys, int xeye, int p1, int p2){
    int xa, xb, xc, xd, ya, yb, yc, yd;
    double s1, t1, s2, t2;

    s1 = (xa - xb) * (yc - ya) - (ya - yb) * (xc - xa);
	t1 = (xa - xb) * (yd - ya) - (ya - yb) * (xd - xa);

    s2 = (xc - xd) * (ya - yc) - (yc - yd) * (xa - xc);
    t2 = (xc - xd) * (yb - yc) - (yc - yd) * (xb - xc);

    if (s1 * t1 <= 0 && s2 * t2 <= 0) {
        return 1;
    }
    return 0;
}





int main(void)
{
    int n;
    int o;
    int count = 0;
    printf("頂点数を入力: ");
    scanf("%d", &n);
    printf("\n");
    printf("障害物数を入力: ");
    scanf("%d", &o);
    printf("\n");
    int matrix[n][n];
    int dfnum[n];
    int vv[n][2];
    int ss[o][2];
    int ee[o][2];

    srand((unsigned int)time(NULL));
    printf("頂点座標\n");
    for (int i = 0; i < n; i++)
    {
        for (int j = 0; j < 2; j++)
        {
            vv[i][j] = rand() % 100 + 1;
        }
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

    printf("\n障害物座標範囲\n");
    for (int i = 0; i < o; i++)
    {
        for (int j = 0; j < 2; j++)
        {
            ss[i][j] = rand() % 100 + 1;
        }
        printf("(xs, xy) = (%d, %d)\n", ss[i][0], ss[i][1]);

        for (int j = 0; j < 2; j++)
        {
            ee[i][j] = rand() % 100 + 1;
        }
        printf("(xe, xe) = (%d, %d)\n", ee[i][0], ee[i][1]);
    }
    
    printf("\n");
    for (int i = 0; i < n; i++)
    {
        dfnum[i] = 0;
    }

    dfs(0, n, dfnum, vv, count);

    return 0;
}
