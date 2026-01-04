#pragma once

#if defined(_WIN32) || defined(__WIN32__)
    #if defined(SIMPLE_PY_EXPORT)
        #define SIMPLE_PY_API __declspec(dllexport)
    #elif defined(SIMPLE_PY_IMPORT)
        #define SIMPLE_PY_API __declspec(dllimport)
    #else
        #define SIMPLE_PY_API
    #endif
#else
    #if defined(SIMPLE_PY_EXPORT)
        #define SIMPLE_PY_API __attribute__((visibility("default")))
    #else
        #define SIMPLE_PY_API
    #endif
#endif