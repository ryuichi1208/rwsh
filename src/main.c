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

int main (int argc, char **argv){
	char *cmd  = NULL;
	cmd = malloc(MAX_CMD_STRLEN);

	/* オプション解析 */
	parse_opt(argc, argv);

	/* シグナル関連処理 */
	if(signal_handler_control(1) != 0)
    		perror("signal handler set failed");

	/* デバッグレベル設定 */
	if(debag_level)
		fprintf(stdout, "debag mode ON\n");

	/* 入力を受け付けコマンドとして実行 */
	while (get_line(cmd, MAX_CMD_STRLEN)) {
		if (!strcmp(cmd, "exit\n")) {
			fprintf(stdout , "logout...\n");
			exit(0);
		} else if (!strcmp(cmd, "debag\n")) {
			fprintf(stdout, "debag");
		} else if (!strcmp(cmd, "cd\n")) {
			_chdir(cmd);
		} else {
			system(cmd);
		}
	}

	return 0;
}
