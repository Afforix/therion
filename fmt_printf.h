#pragma once

#include <fmt/printf.h>

extern template void fmt::detail::vprintf<char, fmt::basic_printf_context<char>>(buffer<char>& buf, basic_string_view<char> format,
             basic_format_args<fmt::basic_printf_context<char>> args);
extern template int fmt::vfprintf<char>(
    std::FILE* f, basic_string_view<char> fmt,
    basic_format_args<basic_printf_context<type_identity_t<char>>> args);
