//Name: chall.c
//Compile: gcc chall.c -o chall -no-pie -fno-stack-protector

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

int main(int argc, char *argv[]){
        if(argc == 2){
                char filename[10];
                char cmd[20];
                int ruid = 0;
                int euid = 0;
                memcpy(filename, argv[1], sizeof(filename));
                snprintf(cmd, 19, "cat %s", filename);
                printf("Your ruid : \n");
                scanf("%d", &ruid);
                printf("Your euid : \n");
                scanf("%d", &euid);
                if(ruid == getuid() && euid == geteuid()) {
                    setreuid(geteuid(), geteuid());
                    printf("Your ruid : %d Your euid : %d\n", getuid(), geteuid());
                    system(cmd);                   
                } else {
                    printf("No.\n");
                }

        }
        else {
            printf("argument...\n");
        }
        return 0;
}
