# Link getopt on Windows when using MSVC and vcpkg.
add_library(getopt-interface INTERFACE)

if (MSVC)
    find_package(unofficial-getopt-win32 REQUIRED)
    target_link_libraries(getopt-interface INTERFACE unofficial::getopt-win32::getopt)
endif()
