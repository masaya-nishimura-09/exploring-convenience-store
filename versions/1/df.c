#include <stdio.h>

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

int main(void)
{
    int n;

    printf("頂点数を入力: ");
    scanf("%d", &n);

    int matrix[n][n];

    int dfnum[n];

    for (int i = 0; i < n; i++)
    {
        for (int j = 0; j < n; j++)
        {
            int a;
            printf("v%dとv%dは隣接か。 0 or 1: \n", i + 1, j + 1);
            scanf("%d", &a);
            matrix[i][j] = a;
        }
        
    }

    for (int i = 0; i < n; i++)
    {
        dfnum[i] = 0;
    }

    dfs(0, n, matrix, dfnum);

    return 0;
}
