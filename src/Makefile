CC = gcc
CFLAGS = -Wall -g -O -I ../include 
SRCS = $(wildcard *.c)
OBJS = $(SRCS:.c=.o)

TARGET = rwsh

$(TARGET): $(OBJS)
	$(CC) $(CFLAGS) -o $@ $^

clean:
	$(RM) $(TARGET) $(OBJS) *~
