h17772
s 00002/00000/00042
d D 1.4 02/12/18 02:37:27 gunnar 4 3
c vpfmt() added
e
s 00007/00007/00035
d D 1.3 02/12/18 01:14:02 gunnar 3 2
c pfmt() functionality improved
e
s 00005/00000/00037
d D 1.2 02/11/03 16:30:26 gunnar 2 1
c change notices added
e
s 00037/00000/00000
d D 1.1 02/11/03 15:54:48 gunnar 1 0
c date and time created 02/11/03 15:54:48 by gunnar
e
u
U
t
T
I 2
/*
 * Changes by Gunnar Ritter, Freiburg i. Br., Germany, November 2002.
 *
 * Sccsid %W% (gritter) %G%
 */
E 2
I 1
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
/* stubbed-out version of <pfmt.h> */

#include <stdio.h>
I 4
#include <stdarg.h>
E 4

D 3
#define MM_ERROR	0
#define MM_ACTION	0
#define MM_WARNING	0
#define MM_INFO		0
#define	MM_NOGET	0
#define MM_NOSTD	0
E 3
I 3
#define MM_ERROR	00
#define MM_ACTION	01
#define MM_WARNING	02
#define MM_INFO		04
#define	MM_NOGET	010
#define MM_NOSTD	020
E 3

#define gettxt(n, s)	s
#define setcat(s)	s
D 3
#define setlabel(s)	0
E 3

I 3
extern int setlabel(const char *);
E 3
extern int pfmt(FILE *, long, const char *, ...);
I 4
extern int vpfmt(FILE *, long, const char *, va_list);
E 4
E 1
