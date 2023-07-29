// Name: chall.c
// Compile Option: gcc chall.c -o chall -fno-stack-protector

#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <unistd.h>
#include <string.h>
#include <fcntl.h>

#define FLAG_SIZE 0x45

void alarm_handler() {
    puts("TIME OUT");
    exit(-1);
}

void initialize() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);

    signal(SIGALRM, alarm_handler);
    alarm(30);
}


int main(int argc, char *argv[]) {
    char cmd[50];
    char input[21];
    char filter[] = {'&', ';', '|', '$', '`', '*','[', ']', '{', '}', '\\', '^', '~', '?', '#', '!'};

    initialize();
    system("ls -al");
    printf("Input Command: \n");
    scanf("%20[^\n]", input);

    // filtering
    for (int i = 0; i < strlen(input); i++){
        for (int j = 0; j < sizeof(filter); j++){
            if(input[i] == filter[j]){
                printf("filtered.\n");
                exit(0);
            }
        }
    }

    snprintf(cmd, 49, "(%s) > /dev/null", input);

    system(cmd);
    system("cat ./out");
    printf("Terminated\n");

    return 0;
}