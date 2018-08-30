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

void exec_cmd(char **argcmd) {
	char **envp;

	if (execve(argcmd[0], argcmd, envp) == -1)
		perror("not cmd");
	exit(0);
}

int main (int argc, char **argv){
	char *cmd = NULL;
	pid_t pid = 0;
	int status;
	char *argcmd[3] = {"/bin/ls", "-l", NULL};

	parse_opt(argc, argv);

	cmd = malloc(MAX_CMD_STRLEN);

	if(signal_handler_control(1) != 0)
    		perror("signal handler set failed");

	if(debag_level)
		fprintf(stdout, "debag mode ON\n");


	while (get_line(cmd, MAX_CMD_STRLEN)) {
		pid = fork();
		if (pid < 0) {
			perror("fork failed");
		} else if (pid == 0) {
			exec_cmd(argcmd);
		} else {
			wait(&status);
		}
	}

	return 0;
}
