# link with this interface library to enable warnings, used for project code
add_library(enable-warnings INTERFACE)
target_compile_options(enable-warnings INTERFACE -Wall -Wextra)

# link with this interface library to disable warnings, used for extern libraries
add_library(disable-warnings INTERFACE)
target_compile_options(disable-warnings INTERFACE -w)

# Fail build if there are warnings, for CI pipelines.
option(ENABLE_WERROR "Treat warnings as errors." OFF)
if (ENABLE_WERROR)
    target_compile_options(enable-warnings INTERFACE -Werror)
endif()
