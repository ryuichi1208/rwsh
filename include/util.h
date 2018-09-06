typedef struct {
	size_t size;
	char *data;
} string_t;

typedef struct {
	size_t size, reserved;
	void **data;
} vector_t;

vector_t *types;
vector_t *delimiters;
