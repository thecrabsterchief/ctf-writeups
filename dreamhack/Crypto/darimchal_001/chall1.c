#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define JOKER "\x40\x53\x06\x03\x43\x52\x54\x3b"
#define KEY   "023661dd4\0"
#define TRUE  1
#define FALSE 0
#define OK    0
#define ERRO -1

void __print_sw_title (char *sw_name);
int __is_valid_pwd (char *pwd);
char *__obfuscation (char *pwd, char *key);
void __create_tag (char *id);

int main (int argc, char *argv[]) {
  if (argc != 2) {
    __print_sw_title(argv[0]);
    return ERRO;
  }

  if ( __is_valid_pwd(argv[1]) ) {
    __create_tag(argv[0]);
    printf("\n +-+ 무, 무슨... 말도 안돼!! 어떻게 복호화 키를...?? +-+ \n");
  } else {
    printf("\n 너의 파일들은 이제 요단강을 건너다가 저승사자와 하이파이브를 하게되었다! 으하하하하!\n"); // ㅋㅋㅋㅋㅋㅋ
  }

  return OK;
}

int __is_valid_pwd (char *pwd) {
  if (! strncmp(JOKER, __obfuscation(pwd, KEY), sizeof(JOKER)) ) {
    return TRUE;
  }

  return FALSE;
}

char *__obfuscation (char *pwd, char *key) {
  int i;
  for (i = 0; i < strlen(pwd); i++) {
    if(key[i] == '\0') break;
    pwd[i] = pwd[i] ^ key[i];
  }

  return pwd;
}

void __print_sw_title (char *sw_name) {
  printf(" ----------- [%s] ----------- \n", sw_name);
  printf(" ::. 복호화 방법: %s <복호화키>\n\n", sw_name);
}

void __create_tag (char *id) {
  FILE *fd;
  char *tag_name = (char *)malloc(24 * sizeof(char));
  memset(tag_name, '\0', 24);
  snprintf(tag_name,24, "./%s.success", id);
  fd = fopen(tag_name, "w");
  if (fd != NULL) {
    fprintf(fd, "복호화가 완료되었습니다.\n");
    fclose(fd);
  } else {
    printf("[ }{4k3r m3ss493 ] Hey sussy baka~ 7h3r3 w4s 4n 3rr0r 0p3nin9 7h3 file..\n");
  }
}
