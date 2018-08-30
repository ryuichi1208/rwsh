#include "main.h"

char* get_line(char *s, int size, char *usr_name) {
	fprintf(stdout, "%s", SHELL);

	while(fgets(s, size, stdin) == NULL) {
		if(errno == EINTR)
 			continue;
 		return NULL;
	}

	return s;
}
