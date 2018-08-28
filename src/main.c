#include "main.h"

static u_int verbose = 0;
static u_int debag_level = 0;

/* usage */
void usage() {
	fprintf(stderr, "rwsh -v level\n");
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

int main (int argc, char **argv) {
	char cmd[MAX_CMD_STRLEN] = {0};

	parse_opt(argc, argv);

	if(signal_handler_control(1) != 0)
    		perror("signal handler set failed");

	if(debag_level)
		fprintf(stdout, "debag mode ON\n");

	while (get_line(cmd, MAX_CMD_STRLEN)) {
	}

	return 0;
}
