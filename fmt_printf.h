#pragma once

#include <fmt/printf.h>

extern template int fmt::vfprintf<char>(
    std::FILE* f, basic_string_view<char> fmt,
    basic_format_args<basic_printf_context<type_identity_t<char>>> args);
