#define _POSIX_C_SOURCE 199309L
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>
#include <stdint.h>

#define BILLION 1000000000L

// return comparisons_count;
int verifica_algo(int n){
    int i, j, k, l;
    
    int comparisons_count = 0;
    int i_c[n], j_c[n], k_c[n];

    for(int i = 0; i < n; i++){
        i_c[i] = 0;
        j_c[i] = 0;
        k_c[i] = 0;
    }

    for (l=1; l<=10000; l++) {
        for(i=1; i <= n-5; i++) {
            for (j=i+2; j<=n/2; j++) {
                for (k=1; k <= n; k++) {
                    comparisons_count++;
                    i_c[i-1] += 1;
                    j_c[i-1] += 1;
                    k_c[i-1] += 1;
                    // printf("%d %d %d %d\n", i, j, k, l);
                }
            }
        }
    }

    for(int i = 0; i < n; i++){
        printf("%d(i) : %d %d %d\n", i, i_c[i], j_c[i], k_c[i]);
    }
    return comparisons_count;
}

int main(int argc, char* argv[]) {
    if (argc != 2) {
        printf("Should have 1 argument (n). Current have %d.\n", argc-1);
        return 1;
    }
    int n = atoi(argv[1]);
    
    // measure execution time:
    uint64_t diff;
    struct timespec start, end;

    clock_gettime(CLOCK_MONOTONIC, &start);
    int total_comparisons = verifica_algo(n);
    clock_gettime(CLOCK_MONOTONIC, &end);
    // print_arr(numbers, n);

    diff = BILLION * (end.tv_sec - start.tv_sec) + end.tv_nsec - start.tv_nsec;
    // printf("%d,%d\n", n, total_comparisons);
    // write_csv(n, total_comparisons);
    printf("{\"n\":%d, \"total_comparisons\":%d, \"execution_time(ns)\":%llu}\n", n, total_comparisons, (long long unsigned int) diff);

    return 0;
}