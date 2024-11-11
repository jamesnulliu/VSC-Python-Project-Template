#pragma once

#if defined(_WIN32) || defined(__WIN32__)
    #if defined(VSC_CPP_TEMPLATE_EXPORT)
        #define VSC_CPP_TEMPLATE_API __declspec(dllexport)
    #elif defined(VSC_CPP_TEMPLATE_IMPORT)
        #define VSC_CPP_TEMPLATE_API __declspec(dllimport)
    #else
        #define VSC_CPP_TEMPLATE_API
    #endif
#else
    #if defined(VSC_CPP_TEMPLATE_EXPORT)
        #define VSC_CPP_TEMPLATE_API __attribute__((visibility("default")))
    #else
        #define VSC_CPP_TEMPLATE_API
    #endif
#endif