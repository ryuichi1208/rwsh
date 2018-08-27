/* ヘッダーファイル */
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/wait.h>
#include <fcntl.h>
#include <signal.h>

/* 定数　*/
#define MAX_CMD_STRLEN 256
#define MIN_CMD_STRLEN 3

/* 関数プロトタイプ */
int 	signal_handler_control(int);
void 	sig_handler(int);
