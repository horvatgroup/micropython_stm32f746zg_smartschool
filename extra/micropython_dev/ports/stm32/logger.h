#ifndef LOGGER_H
#define LOGGER_H

#include <stdio.h>
#include <stdlib.h>
#include <stdarg.h>
#include <stdbool.h>

#define TAG_LOG_ERROR "[1;31m" "ERROR: " "[0m"
#define TAG_LOG_WARNING "[1;33m" "WARNING: " "[0m"

#define __FILENAME__ (strrchr(__FILE__, '/') ? strrchr(__FILE__, '/') + 1 : __FILE__)

#define loggi(format, ...) LoggerPrintf("[%s] " format , __FILENAME__, ##__VA_ARGS__)
#define loggie(format, ...) LoggerPrintf("[%s] " TAG_LOG_ERROR format , __FILENAME__, ##__VA_ARGS__)
#define loggiw(format, ...) LoggerPrintf("[%s] " TAG_LOG_WARNING format , __FILENAME__, ##__VA_ARGS__)
#define loggit(tag, format, ...) LoggerPrintf("[" tag "][%s] " format , __FILENAME__, ##__VA_ARGS__)

#define loggif(format, ...) LoggerPrintf("[%s:%s] " format , __FILENAME__, __FUNCTION__, ##__VA_ARGS__)
#define loggife(format, ...) LoggerPrintf("[%s:%s] " TAG_LOG_ERROR format , __FILENAME__, __FUNCTION__, ##__VA_ARGS__)
#define loggifw(format, ...) LoggerPrintf("[%s:%s] " TAG_LOG_WARNING format , __FILENAME__, __FUNCTION__, ##__VA_ARGS__)
#define loggift(tag, format, ...) LoggerPrintf("[" tag "][%s:%s] " format , __FILENAME__, __FUNCTION__, ##__VA_ARGS__)

#define loggifl(format, ...) LoggerPrintf("[%s:%s:%d] " format , __FILENAME__, __FUNCTION__, __LINE__, ##__VA_ARGS__)
#define loggifle(format, ...) LoggerPrintf("[%s:%s:%d] " TAG_LOG_ERROR format , __FILENAME__, __FUNCTION__, __LINE__, ##__VA_ARGS__)
#define loggiflw(format, ...) LoggerPrintf("[%s:%s:%d] " TAG_LOG_WARNING format , __FILENAME__, __FUNCTION__, __LINE__, ##__VA_ARGS__)
#define loggiflt(tag, format, ...) LoggerPrintf("[" tag "][%s:%s:%d] " format , __FILENAME__, __FUNCTION__, __LINE__, ##__VA_ARGS__)

#define loggf(format, ...) LoggerPrintf(format, ##__VA_ARGS__)
#define loggfe(format, ...) LoggerPrintf(TAG_LOG_ERROR format, ##__VA_ARGS__)
#define loggfw(format, ...) LoggerPrintf(TAG_LOG_WARNING format, ##__VA_ARGS__)
#define loggft(tag, format, ...) LoggerPrintf("[" tag "] " format, ##__VA_ARGS__)
#define loggfet(tag, format, ...) LoggerPrintf("[" tag "] " TAG_LOG_ERROR format, ##__VA_ARGS__)
#define loggfwt(tag, format, ...) LoggerPrintf("[" tag "] " TAG_LOG_WARNING format, ##__VA_ARGS__)

#define loggb(data, len, separator) LoggerPrintBytes(data, len, separator, false)
#define loggbln(data, len, separator) LoggerPrintBytes(data, len, separator, true)
#define loggbex(data, len, prefix, suffix, separator, indexing, newLine) LoggerPrintBytesExtended(data, len, prefix, suffix, separator, indexing, newLine)
#define logga(data, len) LoggerPrintAscii(data, len, false)
#define loggaln(data, len) LoggerPrintAscii(data, len, true)


void LoggerPrintf(const char *format, ...);

void LoggerPrintAscii(const void *object, size_t size, bool newLine);

void LoggerPrintBytes(const void *object, size_t size, char separator, bool newLine);

#endif //LOGGER_H
