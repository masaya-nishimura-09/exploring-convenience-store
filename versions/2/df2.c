#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>


// 2点間の距離を求める
double dist(int x1, int y1, int x2, int y2)
{
    return (sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1)));
}

void dfs(int v, int n, int dfnum[], int vv[][2], int count)
{
    printf("v%dを訪問。\n", v + 1);
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
int main(void)
{
    int n;
    int count = 0;
    printf("頂点数を入力: ");
    scanf("%d", &n);
    int dfnum[n];
    int vv[n][2];

    // // 1から100までの乱数を発生
    // int a = rand() % 100 + 1;

    // 全ての点の座標を作成
    srand((unsigned int)time(NULL));
    for (int i = 0; i < n; i++)
    {
        for (int j = 0; j < 2; j++)
        {
            vv[i][j] = rand() % 100 + 1;
        }
        printf("v%d(%d, %d)\n", i + 1, vv[i][0], vv[i][1]);
    }

    for (int i = 0; i < n; i++)
    {
        dfnum[i] = 0;
    }

    dfs(0, n, dfnum, vv, count);

    return 0;
}
