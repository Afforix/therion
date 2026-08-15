/**
 * @file thchenc.cxx
 */
  
/* Copyright (C) 2000 Stacho Mudrak
 * 
 * $Date: $
 * $RCSfile: $
 * $Revision: $
 *
 * -------------------------------------------------------------------- 
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301 USA
 * --------------------------------------------------------------------
 */
 
#include "thchenc.h"
#include "thchencdata.h"
#include "thchencdatatable.h"
#include "therion.h"
#include "thexception.h"
#include "thparse.h"

#include <cassert>
#include <fmt/format.h>

void thencode(std::string * dest, const char * src, int srcenc)
{
  *dest = thencode(src, srcenc);
}

std::string thencode(const char * src, int srcenc)
{
  assert(src != nullptr);

  // check if source is not UTF-8
  if (srcenc == TT_UTF_8) {
    return src;
  }
  
  std::string dest;
  dest.reserve(strlen(src) * 2);
  
  for (auto srcp = reinterpret_cast<const unsigned char *>(src); *srcp; ++srcp) {
  
    // check if encoding isn't needed
    if (*srcp < thchenc_facc) {
      dest.push_back(*srcp);
    }
    // we have to encode
    else {

      const auto dch = thencode_tbl[*srcp - thchenc_facc][srcenc];

      // two byte UTF-8 character
      if (dch < 0X800) {
        dest.push_back(192 + (dch / 64));
        dest.push_back(128 + (dch % 64));
      }

      // three byte UTF-8 character
      else if (dch < 0X10000) {
        dest.push_back(224 + (dch / 4096));
        dest.push_back(128 + ((dch % 4096) / 64));
        dest.push_back(128 + (dch % 64));
      } 
      
      // longer chars not supported
      else
        therror("unicode character over 0xFFFF not supported");
    }
  }
  
  return dest;
}

 
void thdecode(std::string * dest, int destenc, const char * src)
{
  *dest = thdecode(destenc, src);
}

std::string thdecode(int destenc, const char * src)
{
  assert(src != nullptr);

  // chack if source is not UTF-8
  if (destenc == TT_UTF_8) {
    return src;
  }
  
  std::string dest;
  dest.reserve(strlen(src));
  char32_t sch = 0;    
  
  for (auto srcp = reinterpret_cast<const unsigned char *>(src); *srcp; ++srcp) {
  
    // check if decoding isn't needed
    if (*srcp < thchenc_facc)
      dest.push_back(*srcp);
    // we have to decode
    else {
      // one byte character
      if (*srcp < 0X7F)
        sch = static_cast<char32_t>(*srcp);
      // two byte character
      else if ((*srcp / 32) == 6) {
        sch = 64 * (*srcp % 32);
        srcp++;
        if (*srcp < 128)
          therror(fmt::format("invalid UTF-8 string -- \"{}\"",src));
        sch += *srcp % 64;
      }
      // three byte UTF-8 character
      else if ((*srcp / 16) == 14) {
        sch = 4096 * (*srcp % 16);
        srcp++;
        if (*srcp < 128)
          therror(fmt::format("invalid UTF-8 string -- \"{}\"",src));
        sch += 64 * (*srcp % 64);
        srcp++;
        if (*srcp < 128)
          therror(fmt::format("invalid UTF-8 string -- \"{}\"",src));
        sch += *srcp % 64;
      } 
      
      // longer chars not supported
      else
        therror(fmt::format("invalid UTF-8 string -- \"{}\"",src));
        
      // now we have whchar_t value of UTF-8 character in sch
      if (sch < thchenc_fucc)
        dest.push_back(sch);
      else {
      
        // let's binsearch it's position in the table
        long a = 0, b = (unsigned long)thdecode_tbl_size, x, ix = -1, r, sv = (unsigned long)sch;
        while (a <= b) {
          x = (unsigned long)((a + b) / 2);
          r = sv - long(thdecode_tbl_idx[x]);
          if (r == 0) {
            ix = x;
            break;
          }
          if (r > 0)
            a = x + 1;
          else
            b = x - 1;
        }

        if (ix == -1)
          dest.push_back(thdecode_undef);
        else
          dest.push_back(thdecode_tbl[ix][destenc]);
      }  
    }  // end of decoding
  }

  return dest;
}


void thprint_encodings()
{
  for(int i = 0; i <= TT_UTF_8; i++) {
    thprint(fmt::format("{}\n", thtt_encoding[i].s));
  }
}


int thparse_encoding(char * encstr)
{
  int eid = thmatch_token(encstr, thtt_encoding);
  if (eid == TT_UNKNOWN_ENCODING)
    throw thexception(fmt::format("invalid encoding -- {}", encstr));
  return eid;
}
