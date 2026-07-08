add_library(QuickHull STATIC)
target_sources(QuickHull
    PRIVATE
        QuickHull.cpp
    PUBLIC
        FILE_SET CXX_MODULES
        FILES
            QuickHull.cppm
)
target_link_libraries(QuickHull PRIVATE disable-warnings)
set_target_properties(QuickHull PROPERTIES CXX_CLANG_TIDY "")
