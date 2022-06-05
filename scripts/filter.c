#include <stdio.h>

int main() {
    double current = 0, CPUpercentage = 0;
    char  inputNetwork[1000], outputNetwork[1000];
    while (scanf("%lf %% | %s / %s", &current, inputNetwork, outputNetwork) != EOF) {
        if (current > CPUpercentage) 
            CPUpercentage = current;
    }

    printf("%lf %% | %s / %s\n", CPUpercentage, inputNetwork, outputNetwork);
}