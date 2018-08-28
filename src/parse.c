#include "main.h"

char* get_line(char *s, int size) {
	printf(SHELL);

	while(fgets(s, size, stdin) == NULL) {
		if(errno == EINTR)
 			continue;
 		return NULL;
	}

	return s;
}
