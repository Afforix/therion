/**
 * @file thfiles.cxx
 * File processing module.
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

#include "thlogfile.h"
#include "therion.h"
#include <string.h>

const char * logfilemode = "w";

thlogfile::thlogfile()
{
  this->file_name = "therion.log";
  this->fileh = NULL;
  this->is_open = false;
  this->is_warned = false;
  this->is_logging = true;
}

thlogfile::~thlogfile()
{
  this->close_file();
}


void thlogfile::open_file()
{

  bool should_warn = false;
  if ((!this->is_open) && (!this->is_warned)) {
    this->fileh = fopen(this->get_file_name(), logfilemode);
    if (this->fileh == NULL) {
      if (!this->is_warned) {
        should_warn = true;
        this->is_warned = true;
      }
    }
    else {
      logfilemode = "a";
      this->is_open = true;
      this->is_warned = false;
    }
  }
  
  if (should_warn)
    thwarning(("can't open log file for output -- %s",this->get_file_name()));
}


void thlogfile::close_file()
{
  if (this->is_open) {
    fclose(this->fileh);
    this->is_open = false;
    this->is_warned = false;
  }
}
  
void thlogfile::print(std::string_view msg)
{
  if (this->is_logging) {
    if (!this->is_open)
      this->open_file();
    if (this->is_open) {
      fmt::print(this->fileh, "{}", msg);
      if (std::fflush(this->fileh) != 0)
        this->log_error();
    }
  }
}

void thlogfile::set_file_name(const char *fname)
{
  size_t fnl = strlen(fname);
  if ((!this->is_open) && (fnl > 0))
    this->file_name = fname;
}

const char* thlogfile::get_file_name()
{
    return this->file_name;
}

void  thlogfile::set_logging(bool log_io)
{
  this->is_logging = log_io;
}

bool thlogfile::get_logging()
{
  return(this->is_logging);
}
   
void thlogfile::logging_on()
{
  this->is_logging = true;
}
   
void thlogfile::logging_off()
{
  this->is_logging = false;
}

FILE * thlogfile::get_fileh()
{
  if (!this->is_open)
    this->open_file();
  return this->fileh;
}

void thlogfile::log_error() {
	this->close_file();
	this->logging_off();
	fprintf(stderr,"error -- unable to write to log file (disk full?, insufficient permissions?)\n");
}

thlogfile& get_thlogfile()
{
  static thlogfile log; // global instance
  return log;
}


