# Find all DLL dependencies to deploy on Windows.

# remove addendum release number from the ImageMagick version
string(REGEX MATCH "^[^-]+" ImageMagick_VERSION "${ImageMagick_VERSION}")

# list additional ImageMagick coders we want to deploy
set(ImageMagick_CODERS_PREFIX "$ENV{MSYSTEM_PREFIX}/lib/ImageMagick-${ImageMagick_VERSION}/modules-Q16HDRI/coders")
set(ImageMagick_CODERS
    "${ImageMagick_CODERS_PREFIX}/gif.dll"
    "${ImageMagick_CODERS_PREFIX}/jpeg.dll"
    "${ImageMagick_CODERS_PREFIX}/jxl.dll"
    "${ImageMagick_CODERS_PREFIX}/png.dll"
    "${ImageMagick_CODERS_PREFIX}/webp.dll"
)

# silence warnings about normalizing paths
cmake_policy(SET CMP0207 NEW)

file(GET_RUNTIME_DEPENDENCIES
    EXECUTABLES ${THERION} ${LOCH}
    LIBRARIES ${ImageMagick_CODERS}
    RESOLVED_DEPENDENCIES_VAR DLLS
    PRE_EXCLUDE_REGEXES "^api-ms-" "^ext-ms-"
    POST_EXCLUDE_REGEXES ".*system32/.*\\.dll"
    DIRECTORIES $ENV{PATH}
)

file(MAKE_DIRECTORY ${DLLS_DIR})

foreach(DLL ${DLLS} ${ImageMagick_CODERS})
    message("Copying dependency: ${DLL}")
    file(COPY ${DLL} DESTINATION ${DLLS_DIR})
endforeach()
