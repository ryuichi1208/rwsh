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

#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/un.h>

int main(void)
{
    // サーバーソケット作成
    int sock = socket(AF_UNIX, SOCK_STREAM, 0);
    if (sock == -1)
    {
        perror("socket");
        return 1;
    }

    // struct sockaddr_un 作成
    struct sockaddr_un sa = {0};
    sa.sun_family = AF_UNIX;
    strcpy(sa.sun_path, "/tmp/unix-domain-socket");

    // 既に同一ファイルが存在していたら削除
    remove(sa.sun_path);

    // バインド
    if (bind(sock, (struct sockaddr*) &sa, sizeof(struct sockaddr_un)) == -1)
    {
        perror("bind");
        goto bail;
    }

    // リッスン
    if (listen(sock, 128) == -1)
    {
        perror("listen");
        goto bail;
    }

    while (1)
    {
        // クライアントの接続を待つ
        int fd = accept(sock, NULL, NULL);
        if (fd == -1)
        {
            perror("accept");
            goto bail;
        }

        // 受信
        char buffer[4096];
        int recv_size = read(fd, buffer, sizeof(buffer) - 1);
        if (recv_size == -1)
        {
            perror("read");
            close(fd);
            goto bail;
        }

        // 受信内容を表示
        buffer[recv_size] = '\0';
        printf("message: %s\n", buffer);

        // ソケットのクローズ
        if (close(fd) == -1)
        {
            perror("close");
            goto bail;
        }
    }

bail:
    // エラーが発生した場合の処理
    close(sock);
    return 1;
}
