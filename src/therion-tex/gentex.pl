#!/usr/bin/perl

sub encodecxx {
  $str = shift;
  $str =~ s/\x0D//g;
  $str =~ s/\x0C//g;
  $str =~ s/\x0A//g;
  $str =~ s/\\/\\\\/g;
  $str =~ s/\n/\\n/g;
  $str =~ s/\t/\\t/g;
  $str =~ s/\"/\\"/g;
  return $str;
}

my ($in_file_name, $out_file_name) = @ARGV;

$thtex_library = "";
open(INPT,$in_file_name);
while ($ln = <INPT>) {
  $thtex_library .= "\n\"" . encodecxx($ln) . "\\n\"";
}
close(INPT);

open(OUTPT,">$out_file_name");
print OUTPT <<ENDOUTPT;
/**
 * \@file thtex.cxx
 *
 * THIS FILE IS GENERATED AUTOMATICALLY, DO NOT MODIFY IT !!!
 */  

#include "thtex.h"

#ifndef THMSVC

const char * thtex_library = $thtex_library;

#else

const char * thtex_library = "\\\\input therion.tex\\n";

#endif
ENDOUTPT
close(OUTPT);
