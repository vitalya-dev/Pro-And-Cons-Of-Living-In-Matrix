/*
 * This code contains changes by
 *      Gunnar Ritter, Freiburg i. Br., Germany, 2002. All rights reserved.
 *
 * Conditions 1, 2, and 4 and the no-warranty notice below apply
 * to these changes.
 *
 *
 * Copyright (c) 1980, 1993
 * 	The Regents of the University of California.  All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 * 1. Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 * 3. All advertising materials mentioning features or use of this software
 *    must display the following acknowledgement:
 * 	This product includes software developed by the University of
 * 	California, Berkeley and its contributors.
 * 4. Neither the name of the University nor the names of its contributors
 *    may be used to endorse or promote products derived from this software
 *    without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS'' AND
 * ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED.  IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS BE LIABLE
 * FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
 * DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
 * OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
 * HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
 * LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
 * OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
 * SUCH DAMAGE.
 *
 *
 * Copyright(C) Caldera International Inc. 2001-2002. All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 *   Redistributions of source code and documentation must retain the
 *    above copyright notice, this list of conditions and the following
 *    disclaimer.
 *   Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 *   All advertising materials mentioning features or use of this software
 *    must display the following acknowledgement:
 *      This product includes software developed or owned by Caldera
 *      International, Inc.
 *   Neither the name of Caldera International, Inc. nor the names of
 *    other contributors may be used to endorse or promote products
 *    derived from this software without specific prior written permission.
 *
 * USE OF THE SOFTWARE PROVIDED FOR UNDER THIS LICENSE BY CALDERA
 * INTERNATIONAL, INC. AND CONTRIBUTORS ``AS IS'' AND ANY EXPRESS OR
 * IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
 * WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED. IN NO EVENT SHALL CALDERA INTERNATIONAL, INC. BE
 * LIABLE FOR ANY DIRECT, INDIRECT INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
 * SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
 * BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
 * WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
 * OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
 * EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 *
 *	@(#)config.h	1.7 (gritter) 4/7/02
 */

/*
 * Configurable settings for the ex editor.
 */

/*
 * Maximum screen size in visual mode.
 *
 * Because the routine "alloca" is not portable, TUBESIZE
 * bytes are allocated on the stack each time you go into visual
 * and then never freed by the system.  Thus if you have no terminals
 * which are larger than 24 * 80 you may well want to make TUBESIZE
 * smaller.  TUBECOLS should stay at 160 since this defines the maximum
 * length of opening on hardcopies and allows two lines of open on
 * terminals like adm3's (glass tty's) where it switches to pseudo
 * hardcopy mode when a line gets longer than 80 characters.
 */
#ifndef VMUNIX
#define TUBELINES       70      /* Number of screen lines for visual */
#define TUBECOLS        160     /* Number of screen columns for visual */
#define TUBESIZE        6000    /* Maximum screen size for visual */
#else	/* VMUNIX */
#define TUBELINES       100
#define TUBECOLS        160
#define TUBESIZE        16000
#endif	/* VMUNIX */

/*
 * Various buffer sizes.
 */
#ifndef	VMUNIX
#define	ESIZE		128	/* Regular expression buffer size */
#define	RHSSIZE		256	/* Size of rhs of substitute */
#define	TAGSIZE		128	/* Tag length */
#define	ONMSZ		64	/* Option name size */
#else	/* VMUNIX */
#define	ESIZE		1024
#define	RHSSIZE		512
#define	TAGSIZE		256
#define	ONMSZ		256
#endif	/* VMUNIX */

/*
 * Intptr_t was introduced by SUSv2, and it is highly necessary to achieve
 * portability between various processors. It is a signed integer type
 * capable of holding pointers: sizeof(intptr_t) == sizeof(char *).
 *
 * Type  Environment Typical systems
 * int   IP16        PDP11, 80286
 * int   ILP32       Most VAX, M68k, IA32, SPARC
 * long  LP32        Some IA32 and M68k
 * long  LP64        64 bit mode of IA64, SPARC v9, and Alpha
 *
 * The argument to the sbrk() system call has this type.
 */
#ifdef	notdef
typedef int	intptr_t;
#endif

/*
 * The following types are specified by POSIX.1.
 */

/*
 * The sizeof operator evaluates to this type.
 */
#ifdef	notdef
typedef	int	size_t;
#endif

/*
 * Process identification numbers as returned by getpid(2).
 */
#ifdef	notdef
typedef int     pid_t;
#endif

/*
 * User identification numbers as returned by getuid(2).
 */
#ifdef	notdef
typedef int     uid_t;
#endif

/*
 * Time values as returned by time(2).
 */
#ifdef	notdef
typedef long    time_t;
#endif

/*
 * File descriptor offsets as returned by lseek(2).
 */
#ifdef	notdef
typedef long    off_t;
#endif

/*
 * Signed size type as returned by read(2) and write(2).
 */
#ifdef	notdef
typedef int     ssize_t;
#endif

/*
 * The __STDC__ macro is used to test for compliance with ANSI C. Some
 * compilers comply to this, but do not define it; the value is never
 * used within ex.
 */
#ifdef	notdef
#define	__STDC__	0
#endif

/*
 * Limit constants.
 */
#ifdef	INT_MAX
#define	LRGINT	INT_MAX		/* largest normal length positive integer */
#else
#define	LRGINT	32767		/* largest normal length positive integer */
#endif

#ifdef	LONG_BIT
#if (LONG_BIT > 32)
#define	MAXOCT	22		/* Maximum octal digits in a long */
#define	BIG	1000000000000000000000UL /* largest power of 10 < uns. long */
#define	MAXDIGS	20		/* number of digits in BIG */
#else	/* LONG_BIT <= 32 */
#define	MAXOCT	11		/* Maximum octal digits in a long */
#define	BIG	1000000000UL	/* largest power of 10 < unsigned long */
#define	MAXDIGS	10		/* number of digits in BIG */
#endif	/* LONG_BIT <= 32 */
#else	/* !LONG_BIT */
#define	MAXOCT	11		/* Maximum octal digits in a long */
#define	BIG	1000000000	/* largest power of 10 < unsigned long */
#define	MAXDIGS	10		/* number of digits in BIG */
#endif	/* !LONG_BIT */
