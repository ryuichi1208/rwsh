#include "main.h"

int signal_handler_control(int is_valid){

	struct sigaction act;
 	
	memset(&act, 0, sizeof(act));
	if (sigemptyset(&(act.sa_mask)) < 0) {
		return 1;
	}

	if(is_valid == 1){
		act.sa_handler = SIG_IGN;
	} else {
		act.sa_handler = SIG_DFL;
	}

	//シグナルマスクを設定
	act.sa_flags |= SA_RESTART;
	act.sa_flags |= SA_NOCLDWAIT;

	//actの条件でSIGINTの設定をする(無視又はデフォルト)
	if (sigaction(SIGINT, &act, NULL) < 0) {
		return 1;
	}

	if (sigaction(SIGTSTP, &act, NULL) < 0) {
	    return 1;
	}

	if (sigaction(SIGTTOU, &act, NULL) < 0) {
	    return 1;
	}

	if (sigaction(SIGTTIN, &act, NULL) < 0) {
	    return 1;
	}
	if (sigaction(SIGCHLD, &act, NULL) < 0) {
	    return 1;
	}

	if(is_valid == 1){
		act.sa_handler = sig_handler;

		if (sigaction(SIGTTOU, &act, NULL) < 0) {
			return 1;
		}

		if (sigaction(SIGTTIN, &act, NULL) < 0) {
			return 1;
		}
	}
	return 0;
}

void sig_handler(int sig){
	tcsetpgrp(STDOUT_FILENO, getpid());
}
