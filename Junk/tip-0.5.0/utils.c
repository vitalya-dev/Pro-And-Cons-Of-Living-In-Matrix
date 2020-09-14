/**************************************************************************
 *   utils.c                                                              *
 *                                                                        *
 *   Copyright (C) 1999 Chris Allegretta                                  *
 *   This program is free software; you can redistribute it and/or modify *
 *   it under the terms of the GNU General Public License as published by *
 *   the Free Software Foundation; either version 1, or (at your option)  *
 *   any later version.                                                   *
 *                                                                        *
 *   This program is distributed in the hope that it will be useful,      *
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of       *
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the        *
 *   GNU General Public License for more details.                         *
 *                                                                        *
 *   You should have received a copy of the GNU General Public License    *
 *   along with this program; if not, write to the Free Software          *
 *   Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.            *
 *                                                                        *
 **************************************************************************/

#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#include "tip.h"
#include "proto.h"
#include "config.h"

/* Lower case a string - must be null terminated */
void lowercase(char *src)
{
    long i = 0;

    while (src[i] != 0) {
	src[i] = (char) tolower(src[i]);
	i++;
    }
}


/* I can't believe I have to write this function */
char *strcasestr(char *haystack, char *needle)
{
    char *localneedle, *localhaystack, *found, *tmp, *tmp2;

    /* Make a copy of the search string and searcgh space */
    localneedle = malloc(strlen(needle) + 2);
    localhaystack = malloc(strlen(haystack) + 2);

    strcpy(localneedle, needle);
    strcpy(localhaystack, haystack);

    /* Make them lowercase */
    lowercase(localneedle);
    lowercase(localhaystack);

    /* Look for the lowercased substring in the lowercased search space -
       return NULL if we didn't find anything */
    if ((found = strstr(localhaystack, localneedle)) == NULL) {
	free(localneedle);
	free(localhaystack);
	return NULL;
    }

    /* Else return the pointer to the same place in the real search space */
    tmp2 = haystack;
    for (tmp = localhaystack; tmp != found; tmp++)
	tmp2++;

    free(localneedle);
    free(localhaystack);
    return tmp2;
}

char *strstrwrapper(char *haystack, char *needle)
{

   if (case_sensitive)
      return strstr(haystack, needle);
   else
      return strcasestr(haystack, needle);
}

/* Strip first newline enocuntered in a string */
void strip_newline(char *str)
{
    char *tmp;

    for (tmp = str; *tmp != '\n' && *tmp != 0; tmp++);

    if (*tmp == '\n')
	*tmp = 0;

    return;
}
