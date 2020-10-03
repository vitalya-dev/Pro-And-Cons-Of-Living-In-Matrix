/*
 *
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
 *	@(#)ex_proto.h	1.15 (gritter) 4/7/02
 */

/*
 * Function type definitions
 */

/* ex.c */
#ifdef	POSIX_1
shand setsig __P((int, shand));
#endif
int init __P((void));
/* ex_addr.c */
int setdot __P((void));
int setdot1 __P((void));
int setcount __P((void));
int getnum __P((void));
int setall __P((void));
int setnoaddr __P((void));
line *address __P((char *));
int setCNL __P((void));
int setNAEOL __P((void));
/* ex_cmds.c */
int commands __P((int, int));
/* ex_cmds2.c */
int cmdreg __P((void));
int endcmd __P((int));
int eol __P((void));
int error __P((char *, ...));
int erewind __P((void));
int fixol __P((void));
int exclam __P((void));
int makargs __P((void));
int next __P((void));
int newline __P((void));
int nomore __P((void));
int quickly __P((void));
int resetflav __P((void));
int serror __P((char *, ...));
int setflav __P((void));
int skipend __P((void));
int tailspec __P((int));
int tail __P((char *));
int tail2of __P((char *));
int tailprim __P((char *, int, int));
int vcontin __P((int));
int vnfl __P((void));
/* ex_cmdsub.c */
int append __P((int (*)(), line *));
int appendnone __P((void));
int pargs __P((void));
int delete __P((int));
int deletenone __P((void));
int squish __P((void));
int join __P((int));
int move __P((void));
int put __P((void));
int pragged __P((int));
int shift __P((int, int));
int tagfind __P((int));
int yank __P((void));
int zop __P((int));
int zop2 __P((int, int));
int plines __P((line *, line *, int));
int pofix __P((void));
int undo __P((int));
int mapcmd __P((int, int));
int cmdmac __P((int));
/* ex_data.c */
/* ex_extern.c */
/* ex_get.c */
int ignchar __P((void));
int getchar __P((void));
int getcd __P((void));
int peekchar __P((void));
int peekcd __P((void));
int gettty __P((void));
line *setin __P((line *));
/* ex_io.c */
int filename __P((int));
int getargs __P((void));
int getone __P((void));
int rop __P((int));
int rop2 __P((void));
int rop3 __P((int));
int wop __P((int));
int getfile __P((void));
int putfile __P((int));
int wrerror __P((void));
int source __P((char *, int));
int clrstats __P((void));
/* ex_put.c */
int (*setlist __P((int))) __P((void));
int (*setnumb __P((int))) __P((void));
int listchar __P((int));
int normchar __P((int));
int numbline __P((int));
int normline __P((void));
int putchar __P((int));
int termchar __P((int));
int flush __P((void));
int flush1 __P((void));
int fgoto __P((void));
int tab __P((int));
int noteinp __P((void));
int termreset __P((void));
int draino __P((void));
int flusho __P((void));
int putnl __P((void));
int putch __P((int));
int putpad __P((char *));
int setoutt __P((void));
int vlprintf __P((char *, va_list));
int lprintf __P((char *, ...));
int putNFL __P((void));
int pstart __P((void));
int pstop __P((void));
int tostart __P((void));
int tostop __P((void));
int gTTY __P((int));
int noonl __P((void));
/* ex_re.c */
int global __P((int));
int substitute __P((int));
int getsub __P((void));
char *place __P((char *, char *, char *));
int compile __P((int, int));
int same __P((int, int));
int execute __P((int, line *));
int advance __P((char *, char *));
/* ex_set.c */
int set __P((void));
/* ex_subr.c */
int any __P((int, char *));
int backtab __P((int));
int change __P((void));
int column __P((char *));
int comment __P((void));
int Copy __P((char *, char *, int));
int copyw __P((line *, line *, int));
int copywR __P((line *, line *, int));
int ctlof __P((int));
int dingdong __P((void));
int fixindent __P((int));
int filioerr __P((char *));
char *genindent __P((int));
int getDOT __P((void));
line *getmark __P((int));
int getn __P((char *));
int ignnEOF __P((void));
int is_white __P((int));
int junk __P((int));
int killed __P((void));
int killcnt __P((int));
int lineno __P((line *));
int lineDOL __P((void));
int lineDOT __P((void));
int markDOT __P((void));
int markpr __P((line *));
int markreg __P((int));
char *mesg __P((char *));
int vmerror __P((char *, va_list));
int merror __P((char *, ...));
int morelines __P((void));
int nonzero __P((void));
int notable __P((int));
int notempty __P((void));
int netchHAD __P((int));
int netchange __P((int));
int printof __P((int));
int putmark __P((line *));
int putmk1 __P((line *, int));
char *plural __P((long));
int qcolumn __P((char *, char *));
int reverse __P((line *, line *));
int save __P((line *, line *));
int save12 __P((void));
int saveall __P((void));
int span __P((void));
int synced __P((void));
int skipwh __P((void));
int vsmerror __P((char *, va_list));
int smerror __P((char *, ...));
char *strend __P((char *));
int strcLIN __P((char *));
int syserror __P((void));
int tabcol __P((int, int));
char *vfindcol __P((int));
char *vskipwh __P((char *));
char *vpastwh __P((char *));
int whitecnt __P((char *));
int markit __P((line *));
int setrupt __P((void));
int preserve __P((void));
int exitex __P((int));
/* ex_tagio.c */
int topen __P((char *, char *));
int tseek __P((int, off_t));
int tgets __P((char *, int, int));
int tclose __P((int));
/* ex_temp.c */
int fileinit __P((void));
int cleanup __P((int));
int getline __P((line));
int putline __P((void));
int tlaste __P((void));
int tflush __P((void));
int synctmp __P((void));
int TSYNC __P((void));
int putreg __P((int));
int partreg __P((int));
int notpart __P((int));
int YANKreg __P((int));
int kshift __P((void));
int regbuf __P((int, char *, int));
/* ex_tty.c */
int gettmode __P((void));
int setterm __P((char *));
int setsize __P((void));
char *fkey __P((int));
int cost __P((char *));
/* ex_unix.c */
int unix0 __P((int));
int filter __P((int));
int recover __P((void));
int waitfor __P((void));
int revocer __P((void));
/* ex_v.c */
int oop __P((void));
int vop __P((void));
int fixzero __P((void));
int savevis __P((void));
int undvis __P((void));
int vsetsiz __P((int));
/* ex_vadj.c */
int vopen __P((line *, int));
int vreopen __P((int, int, int));
int vglitchup __P((int, int));
int vinslin __P((int, int, int));
int vrollup __P((int));
int vup1 __P((void));
int vmoveitup __P((int, int));
int vscrap __P((void));
int vrepaint __P((char *));
int vredraw __P((int));
int vsyncCL __P((void));
int vsync __P((int));
int vsync1 __P((int));
int vreplace __P((int, int, int));
int sethard __P((void));
int vdirty __P((int, int));
/* ex_version.c */
int printver __P((void));
/* ex_vget.c */
int ungetkey __P((int));
int getkey __P((void));
int peekbr __P((void));
int getbr __P((void));
int getesc __P((void));
int peekkey __P((void));
int readecho __P((int));
int setLAST __P((void));
int addtext __P((char *));
int setDEL __P((void));
int setBUF __P((cell *));
int noteit __P((int));
int macpush __P((char *, int));
int vgetcnt __P((void));
/* ex_vmain.c */
int vmain __P((void));
int prepapp __P((void));
int vremote __P((int, int (*)(), int));
int vsave __P((void));
cell *str2cell __P((cell *, char *));
char *cell2str __P((char *, cell *));
cell *cellcpy __P((cell *, cell *));
size_t cellen __P((cell *));
cell *cellcat __P((cell *, cell *));
/* ex_voper.c */
int operate __P((int, int));
int find __P((int));
int word __P((int (*)(), int));
int eend __P((int (*)()));
int wordof __P((int, char *));
int wordch __P((char *));
int margin __P((void));
/* ex_vops.c */
int vUndo __P((void));
int vundo __P((int));
int vmacchng __P((int));
int vnoapp __P((void));
int vmove __P((void));
int vdelete __P((int));
int vchange __P((int));
int voOpen __P((int, int));
int vshftop __P((void));
int vfilter __P((void));
int vrep __P((int));
int vyankit __P((void));
/* ex_vops2.c */
int bleep __P((int, char *));
int vdcMID __P((void));
int takeout __P((cell *));
int ateopr __P((void));
int showmode __P((int));
int vappend __P((int, int, int));
int back1 __P((void));
char *vgetline __P((int, char *, bool *, int));
int vdoappend __P((char *));
/* ex_vops3.c */
int llfind __P((int, int, int (*)(), line *));
int lindent __P((line *));
int lmatchp __P((line *));
int lsmatch __P((char *));
int lnext __P((void));
int lbrack __P((int, int (*)()));
/* ex_vput.c */
int vclear __P((void));
int vclrcell __P((cell *, int));
int vclrlin __P((int, line *));
int vclreol __P((void));
int vclrech __P((int));
int fixech __P((void));
int vcursbef __P((char *));
int vcursat __P((char *));
int vcursaft __P((char *));
int vfixcurs __P((void));
int vsetcurs __P((char *));
int vigoto __P((int, int));
int vcsync __P((void));
int vgotoCL __P((int));
int vgoto __P((int, int));
int vprepins __P((void));
int vputch __P((int));
int vinschar __P((int));
int goim __P((void));
int endim __P((void));
int vputchar __P((int));
int physdc __P((int, int));
/* ex_vwind.c */
int vmoveto __P((line *, char *, int));
int vjumpto __P((line *, char *, int));
int vupdown __P((int, char *));
int vup __P((int, int, int));
int vdown __P((int, int, int));
int vcontext __P((line *, int));
int vclean __P((void));
int vshow __P((line *, line *));
int vroll __P((int));
int vdepth __P((void));
int vnline __P((char *));
/* malloc.c */
char *poolsbrk __P((intptr_t));
/* printf.c */
int printf __P((const char *, ...));
int vprintf __P((const char *, va_list));
char *p_dconv __P((long, char *));

woid onemt __P((int));
woid onhup __P((int));
woid onintr __P((int));
#ifdef	CBREAK
woid vintr __P((int));
#endif
woid onsusp __P((int));
woid onwinch __P((int));
