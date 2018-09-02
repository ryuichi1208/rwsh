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
#include <unistd.h>
#include <errno.h>
#include <getopt.h>

/* alias */
typedef unsigned short u_short;
typedef unsigned int u_int;
typedef unsigned long u_long;

/* 定数　*/
#define MAXPATHLEN	256
#define MAX_CMD_STRLEN 	256
#define MIN_CMD_STRLEN	3
#define SHELL		"rwsh :"

/* 関数プロトタイプ */
int 	signal_handler_control(int);
void 	sig_handler(int);
char*	get_line(char*, int);

typedef enum _job_mode {
	FOREGROUND,
	BACKGROUND,
	STOPPED,
	DEFUNCT
} job_mode;

typedef enum _process_state {
	WAITING,
	RUNNING,
	FINISHED,
} process_state;

typedef enum write_option {
    TRUNC,
    APPEND,
} write_option;

/* プロセス構造体 */
typedef struct _process {
    char*		program_name;
    char*		input_redirection;
    char*		output_redirection;
    char**		argument_list;
    int			pipe[2];
    pid_t		pid;
    process_state	state;
    write_option	output_option;
    struct		process *next;
} process;

/* ジョブ構造体 */
typedef struct _job {
	char*		command;
	int		job_num;
	pid_t		pgid;
	job_mode	mode;
	process*	process_list;
	struct 		job *next;
} job;
