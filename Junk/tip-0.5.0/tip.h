/**************************************************************************
 *   tip.h                                                                *
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


#ifndef TIP_H
#define TIP_H 1

#ifdef HAVE_NCURSES_H
#include <ncurses.h>
#else /* Uh oh */
#include <curses.h> 
#endif

#define VERMSG "GNU TIP v" VERSION

/* Structure types */
typedef struct filestruct {
    char *data;
    struct filestruct *next;	/* Next node */
    struct filestruct *prev;	/* Previous node */
    long bytes;			/* # of Bytes before this line */
    int wrapline;		/* Is this line newly created by a wrap */
} filestruct;

typedef struct shortcut {
   int val;              /* Actual sequence that generates the keystroke */
   char desc[50];       /* Description, e.g. "Page Up" */
} shortcut;

/* Control key sequences, chaning these would be very very bad */

#define TIP_CONTROL_A 1
#define TIP_CONTROL_B 2
#define TIP_CONTROL_C 3
#define TIP_CONTROL_D 4
#define TIP_CONTROL_E 5
#define TIP_CONTROL_F 6
#define TIP_CONTROL_G 7
#define TIP_CONTROL_H 8
#define TIP_CONTROL_I 9
#define TIP_CONTROL_J 10
#define TIP_CONTROL_K 11
#define TIP_CONTROL_L 12
#define TIP_CONTROL_M 13
#define TIP_CONTROL_N 14
#define TIP_CONTROL_O 15
#define TIP_CONTROL_P 16
#define TIP_CONTROL_Q 17
#define TIP_CONTROL_R 18
#define TIP_CONTROL_S 19
#define TIP_CONTROL_T 20
#define TIP_CONTROL_U 21
#define TIP_CONTROL_V 22
#define TIP_CONTROL_W 23
#define TIP_CONTROL_X 24
#define TIP_CONTROL_Y 25
#define TIP_CONTROL_Z 26

/* Some semi-changeable keybindings, dont play with unless you're sure you
know what you're doing */

#define TIP_INSERTFILE_KEY	TIP_CONTROL_R
#define TIP_EXIT_KEY 		TIP_CONTROL_X
#define TIP_WRITEOUT_KEY	TIP_CONTROL_O
#define TIP_GOTO_KEY		TIP_CONTROL_G
#define TIP_WHEREIS_KEY		TIP_CONTROL_W
#define TIP_REPLACE_KEY		TIP_CONTROL_P
#define TIP_PREVPAGE_KEY	TIP_CONTROL_Y
#define TIP_NEXTPAGE_KEY	TIP_CONTROL_V
#define TIP_CUT_KEY		TIP_CONTROL_K
#define TIP_UNCUT_KEY		TIP_CONTROL_U
#define TIP_CURSORPOS_KEY	TIP_CONTROL_C
#define TIP_SPELLING_KEY	TIP_CONTROL_T
#define TIP_FIRSTLINE_KEY	TIP_PREVPAGE_KEY
#define TIP_LASTLINE_KEY	TIP_NEXTPAGE_KEY
#define TIP_CANCEL_KEY		TIP_CONTROL_C
#define TIP_CASE_KEY		TIP_CONTROL_A
#define TIP_REFRESH_KEY		TIP_CONTROL_L
#define TIP_SPELL_KEY		TIP_CONTROL_T


#define MAIN_LIST_LEN 12
#define WHEREIS_LIST_LEN 4
#define REPLACE_LIST_LEN 4
#define GOTO_LIST_LEN 3
#define WRITEFILE_LIST_LEN 1
     
#endif                             
