#include "main.h"

char* get_line(char *s, int size) {
	char path[MAXPATHLEN];

	if(!getcwd(path, sizeof(path))) {
		perror("getcwd failed");
		return "exit";
	}

	fprintf(stdout, "%s %s$ ", SHELL, path);

	while(fgets(s, size, stdin) == NULL) {
		if(errno == EINTR)
 			continue;
 		return NULL;
	}

	return s;
}
