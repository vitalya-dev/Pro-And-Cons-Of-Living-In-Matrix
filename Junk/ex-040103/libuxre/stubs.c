/*
 * Changes by Gunnar Ritter, Freiburg i. Br., Germany, November 2002.
 *
 * Sccsid @(#)stubs.c	1.22 (gritter) 9/22/03
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

#include "colldata.h"

struct lc_collate *
libuxre_lc_collate(struct lc_collate *cp)
{
	static struct lc_collate curinfo = {0}; /* means CHF_ENCODED */

	return &curinfo;
}

#include "wcharm.h"

LIBUXRE_STATIC int
libuxre_mb2wc(w_type *wt, const unsigned char *s)
{
	wchar_t wc;
	int len;

	if ((len = mbtowc(&wc, (const char *)&s[-1], MB_LEN_MAX)) > 0)
		*wt = wc;
	else if (len == 0)
		*wt = '\0';
	else /*if (len < 0)*/
		*wt = WEOF;
	return len > 0 ? len - 1 : len;
}

static const char sccsid[] = "@(#)libuxre	1.22 (gritter) 9/22/03";
