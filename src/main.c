#include "main.h"

static u_int verbose = 0;
static u_int debag_level = 0;

/* usage */
void usage() {
	fprintf(stderr, "usage : rwsh -v level\n");
	exit(1);
}

/* オプション解析用関数 */
void parse_opt(int argc, char **argv) {
	int opt;
	
	while ((opt = getopt(argc, argv, "v:")) != -1) {
		switch (opt) {
			case 'v':
				verbose = 1;
				debag_level = strtol(optarg, NULL, 0);
				break;
			default:
				usage();
				break;
		}
	}
}

/* コマンド実行関数 */
void exec_cmd(char **argcmd, char *cmd) {
	system(cmd);
	exit(0);
}

int main (int argc, char **argv){
	char *cmd = NULL;
	pid_t pid = 0;
	int status;

	/* オプション解析 */
	parse_opt(argc, argv);

	cmd = malloc(MAX_CMD_STRLEN);

	/* シグナル関連処理 */
	if(signal_handler_control(1) != 0)
    		perror("signal handler set failed");

	/* デバッグレベル設定 */
	if(debag_level)
		fprintf(stdout, "debag mode ON\n");


	while (get_line(cmd, MAX_CMD_STRLEN)) {
		pid = fork();
		if (pid < 0) {
			perror("fork failed");
		} else if (pid == 0) {
			exec_cmd(argcmd, cmd);
		} else {
			wait(&status);
		}
	}

	return 0;
}
