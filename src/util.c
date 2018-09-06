#include "main.h"
#include "util.h"

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

void string_set(string_t *str, size_t pos, char c){
	str->data[pos] = c;
}


size_t get_filesize(FILE *fp){
	fseek(fp, 0L, SEEK_END);
	size_t size = ftell(fp);
	fseek(fp, 0L, SEEK_SET);
	return size;
}

string_t* string_new(size_t size){
	string_t *str = (string_t*)malloc(sizeof(string_t));
	str->size = size;
	str->data = (char*)malloc(size);
	if(str->data == NULL) 
		fprintf(stderr, "malloc failed: size=%u", size);
	return str;
}

/* ファイル読み込み関数 */
string_t* read_file(FILE *fp){
	int c;
	size_t i = 0;

	size_t fsize = get_filesize(fp);

	string_t *str = string_new(fsize);

	while(c = fgetc(fp)){
		if(c == EOF) break;
		string_set(str, i, c);
		i++;
	}

	return str;
}

void print_indent(size_t indent){
	size_t i;
	for(i=0;i<indent;i++) putchar(' ');
}

