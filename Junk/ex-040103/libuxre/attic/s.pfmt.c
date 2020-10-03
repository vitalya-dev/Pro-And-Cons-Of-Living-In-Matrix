h36787
s 00090/00000/00000
d D 1.1 02/12/18 02:37:31 gunnar 1 0
c date and time created 02/12/18 02:37:31 by gunnar
e
u
U
t
T
I 1
/*
 * Changes by Gunnar Ritter, Freiburg i. Br., Germany, November 2002.
 *
 * Sccsid %W% (gritter) %G%
 */
/*  UNIX(R) Regular Expresssion Library
 *
 *  Note: Code is released under the GNU LGPL
 *
 *  Copyright (C) 2001 Caldera International, Inc.
 *
 *  This library is free software; you can redistribute it and/or
 *  modify it under the terms of the GNU Lesser General Public
 *  License as published by the Free Software Foundation; either
 *  version 2 of the License, or (at your option) any later version.
 *
 *  This library is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 *  Lesser General Public License for more details.
 *
 *  You should have received a copy of the GNU Lesser General Public
 *  License along with this library; if not, write to:
 *        Free Software Foundation, Inc.
 *        59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
 */
/* stubbed-out routines needed to complete the RE libc code */

#include <stdarg.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "pfmt.h"

static char	*label;

int
vpfmt(FILE *fp, long flags, const char *fmt, va_list ap)
{
	int ret = -1;
	const char	*f = fmt;

	if ((flags&MM_NOGET) == 0) {
		if ((f = strchr(fmt, ':')) == 0)
			return -1;
		if ((f = strchr(f+1, ':')) == 0)
			return -1;
		f++;
	} else
		f = fmt;
	if ((flags&MM_NOSTD) == 0) {
		if (label)
			fprintf(fp, "%s: ", label);
		if (flags&MM_ACTION)
			fprintf(fp, "TO FIX: ");
		else if (flags&MM_WARNING)
			fprintf(fp, "WARNING: ");
		else if (flags&MM_INFO)
			fprintf(fp, "INFO: ");
		else
			fprintf(fp, "ERROR: ");
	}
	if ((ret = vfprintf(fp, f, ap)) < 0)
		ret = -1;
	return ret;
}

int
pfmt(FILE *fp, long flags, const char *fmt, ...)
{
	va_list	ap;
	int	val;

	va_start(ap, fmt);
	val = vpfmt(fp, flags, fmt, ap);
	va_end(ap);
	return val;
}

int
setlabel(const char *s)
{
	if (label)
		free(label);
	if (s && *s)
		label = strdup(s);
	else
		label = NULL;
	return 0;
}
E 1
