#include "main.h"

int _chdir(char *dir) {

	dir = "../";

	if(!chdir(dir)) {
		perror("chdir failed");
		return -1;
	}

	return 0;
}

int _open(char *filepath) {
	return 0;
}
