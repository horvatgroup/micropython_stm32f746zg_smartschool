#include "logger.h"

void LoggerPrintf(const char *format, ...) {
    va_list args;
    va_start(args, format);
    vprintf(format, args);
    va_end(args);
}

void LoggerPrintAscii(const void *object, size_t size, bool newLine) {
    const unsigned char *const bytes = (const unsigned char *const) object;
    size_t i;

    LoggerPrintf("[");
    for (i = 0; i < size; i++) {
        LoggerPrintf("%c", bytes[i]);
    }
    LoggerPrintf("]");
    if (newLine) {
        LoggerPrintf("\n");
    } else {
        LoggerPrintf(" ");
    }
}

void LoggerPrintBytes(const void *object, size_t size, char separator, bool newLine) {
    const unsigned char *const bytes = (const unsigned char *const) object;
    size_t i;

    LoggerPrintf("[");
    for (i = 0; i < size; i++) {
        LoggerPrintf("%02X", bytes[i]);
        if (i < size - 1){
            LoggerPrintf("%c", separator);
        }
    }
    LoggerPrintf("]");

    if (newLine) {
        LoggerPrintf("\n");
    }
}
