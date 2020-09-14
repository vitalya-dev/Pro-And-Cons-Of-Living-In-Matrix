/**************************************************************************
 *   tip.c                                                                *
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

#include <stdio.h>
#include <stdlib.h>
#include <stdarg.h>
#include <signal.h>
#include <unistd.h>
#include <string.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <errno.h>
#include <ctype.h>

#include "tip.h"
#include "proto.h"
#include "config.h"

/* What we do when we're all set to exit */
void finish(int sigage)
{
    blank_bottombars();
    wrefresh(bottomwin);
    endwin();
    exit(0);
}

/* Die (gracefully?) */
void die(char *msg, ...)
{
    va_list ap;
   
    va_start(ap, msg);
    vfprintf(stderr, msg, ap);
    va_end(ap);

    clear();
    refresh();
    resetty();
    endwin();
    printf(msg);
    exit(0);
}

/* Initialize global variables - no better way for now */
void global_init(void)
{
   center_x = COLS / 2;
   center_y = LINES / 2;
   current_x = 0;
   current_y = 0;
   editwinrows = LINES - 5;
   editwineob = editwinrows - 1;
   fileage = NULL;
   cutbuffer = NULL;
}

/* Make a copy of a node to a pointer (space will be malloc()ed */
filestruct *copy_node(filestruct *src)
{
   filestruct *dst;

   dst = malloc(sizeof(filestruct));
   dst->data = malloc(strlen(src->data)+2);

   dst->next = src->next;
   dst->prev = src->prev;
   strncpy(dst->data, src->data, strlen(src->data));

   return dst;
}

/* Unlink a node from the rest of the struct */
void unlink_node(filestruct *fileptr)
{
   if (fileptr->prev != NULL)
      fileptr->prev->next = fileptr->next;
   if (fileptr->next != NULL)
      fileptr->next->prev = fileptr->prev;
}

void delete_node(filestruct *fileptr)
{
   free(fileptr->data);
   free(fileptr);
}


/* Okay, now let's duplicate a whole struct! */
filestruct *copy_filestruct(filestruct *src)
{
   filestruct *dst, *tmp, *head, *prev;

   head = copy_node(src);
   dst = head;			/* Else we barf on copying just one line :-) */
   tmp = src->next;
   prev = head;

   while (tmp != NULL)
   {
      dst = copy_node(tmp);
      dst->prev = prev;
      prev->next = dst;

      prev = dst;
      tmp = tmp->next;
   }

   dst->next = NULL;
   return head;
}

/* Free() a single node */
int free_node (filestruct *src)
{
   if (src == NULL)
      return 0;

   if (src->next != NULL)
      free(src->data);
   free(src);
   return 1;
}

int free_filestruct(filestruct *src)
{
   filestruct *fileptr = src;

   if (src == NULL)
      return 0;

   while (fileptr->next != NULL)
   {
      fileptr = fileptr->next;
      free_node(fileptr->prev);

#ifdef DEBUG
      fprintf(stderr, "free_node(): free'd a note, YAY!\n");
#endif
   }
   free_node(fileptr);
   fprintf(stderr, "free_node(): free'd last node.\n");

   return 1;
}


/* Window I/O */

void reset_cursor(void)
{
  filestruct *ptr = edittop;

  current_y = 0;

  while (ptr != current && ptr != editbot && ptr->next != NULL)
  {
     ptr = ptr->next;
     current_y++;
  }
  wmove(edit, current_y, current_x);
}

void blank_bottombars(void)
{
   int i, j;

   for (j = 1; j <= 2; j++)
      for (i = 0; i <= COLS - 1; i++)
         mvwaddch(bottomwin, j, i, ' ');

  reset_cursor();
}

void blank_statusbar(void)
{
   int i;

   for (i = 0; i <= COLS - 1; i++)
      mvwaddch(bottomwin, 0, i, ' ');

  reset_cursor();
}

void blank_statusbar_refresh(void)
{
  blank_statusbar();
  wrefresh(bottomwin);
}

void check_statblank(void)
{

#ifdef DEBUG
   fprintf(stderr, "statblank = %d\n", statblank);
#endif

   if (statblank > 1)
      statblank--;
   else if (statblank == 1)
   {
      statblank--;
      blank_statusbar_refresh();
   }
}

/* Get the input from the kb, this should only be called from statusq */

int tipgetstr(char *buf, char *def, shortcut s[], int slen, int start_x)
{
    int kbinput = 0, j = 0;
    char inputstr[5], inputbuf[132] = "";

    blank_statusbar();
    mvwaddstr(bottomwin, 0, 0, buf);
    if (strlen(def) > 0)
      waddstr(bottomwin, def);
    wrefresh(bottomwin);

    /* Get the input! */
    if (strlen(def) > 0)
    {
       strcpy(answer, def);
       strcpy(inputbuf, def);
    }

    /* Go into raw mode so we can actually get ^C, for example */
    raw();

    while ((kbinput = wgetch(bottomwin)) != 13)
    {
       for (j = 0; j <= slen - 1; j++)
       {
          if (kbinput == s[j].val)
          {
             noraw();
             cbreak();
             strcpy(answer, "");
             return s[j].val;
          }
       }
       if (kbinput >= 32)
          switch (kbinput)
       {
         case KEY_BACKSPACE: case KEY_DC: case 127:
            if (strlen(inputbuf) > 0)
               inputbuf[strlen(inputbuf)-1] = 0;
            blank_statusbar();
            mvwaddstr(bottomwin, 0, 0, buf);
            waddstr(bottomwin, inputbuf);
            wrefresh(bottomwin);
            break;
         default:
             sprintf(inputstr, "%c", kbinput);
             strncat(inputbuf, inputstr, 132);
             mvwaddstr(bottomwin, 0, 0, buf);
             waddstr(bottomwin, inputbuf);
             wrefresh(bottomwin);

#ifdef DEBUG
             fprintf(stderr, "input \'%c\' (%d)\n", kbinput, kbinput);
#endif
       }
    }

    strncpy(answer, inputbuf, 132);

    noraw();
    cbreak();
    if (!strcmp(answer, ""))
       return -1;
    else
       return 0;
}

void horizbar(WINDOW *win, int y)
{
   int i = 0;

   wattron(win, A_REVERSE);
   for (i = 0; i <= COLS - 1; i++)
      mvwaddch(win, y, i, ' ');
   wattroff(win, A_REVERSE);
}

void titlebar(void)
{
   horizbar(topwin, 0);
   wattron(topwin, A_REVERSE);
   mvwaddstr(topwin, 0, 3, VERMSG);
   mvwaddstr(topwin, 0, center_x - 3, "File: ");
   waddstr(topwin, filename);

   if (modified)
      mvwaddstr(topwin, 0, COLS - 10, "Modified");
   wattroff(topwin, A_REVERSE);
   wrefresh(topwin);
   reset_cursor();
}

void onekey(char *keystroke, char *desc)
{
   char description[80];
   
   snprintf(description, 12, " %-11s", desc);
   wattron(bottomwin, A_REVERSE);
   waddstr(bottomwin, keystroke);
   wattroff(bottomwin, A_REVERSE);
   waddstr(bottomwin, description);
}

void clear_bottomwin(void)
{
   int i;

   for (i = 0; i <= COLS - 1; i++)
   {
      mvwaddch(bottomwin, 1, i, ' ');
      mvwaddch(bottomwin, 2, i, ' ');
   }
   wrefresh(bottomwin);
}

void bottombars(shortcut s[], int slen)
{
   int i;
   char keystr[10];

   clear_bottomwin();
   wmove(bottomwin, 1, 0);
   for (i = 0; i <= slen - 1; i += 2)
   {
      sprintf(keystr, "^%c", s[i].val + 64);
      onekey(keystr, s[i].desc);
   }
   wmove(bottomwin, 2, 0);
   for (i = 1; i <= slen - 1; i += 2)
   {
      sprintf(keystr, "^%c", s[i].val + 64);
      onekey(keystr, s[i].desc);
   }
   wrefresh(bottomwin);

}

/* Just update one line in the edit buffer */
void update_line(filestruct *fileptr)
{
   filestruct *filetmp;
   int line = 0;

  for (filetmp = edittop; filetmp != fileptr && filetmp != editbot; 
       filetmp = filetmp->next)
     line++;

  mvwaddstr(edit, line, 0, filetmp->data);
  wrefresh(edit);

}

void center_cursor(void)
{
   current_y = editwinrows / 2;
   wmove(edit, current_y, current_x);
   wrefresh(edit);
}

/* Refresh the screen without changing the position of lines */
void edit_refresh(void)
{
   int lines = 0, i = 0, j = 0;
   filestruct *temp;

   temp = edittop;
   while (lines <= editwinrows - 1 && lines <= totlines && temp != NULL && temp != filebot)
   {
      mvwaddstr(edit, lines, 0, temp->data);
      temp = temp->next;
      lines++;
   } 

   if (temp == filebot)
   {
      mvwaddstr(edit, lines, 0, filebot->data);
      lines++;
      for (i = lines; i <= editwinrows - 1; i++)
         for(j = 0; j <= COLS - 1; j++)
            mvwaddch(edit, i, j, ' ');

   }
   editbot = temp;

}

/*
 * Nice generic routine to update the edit buffer given a pointer to the
 * file struct =) 
 */
void edit_update(filestruct *fileptr)
{
   int lines = 0, i = 0, j = 0;
   filestruct *temp;

   temp = fileptr;
   while (i <= editwinrows / 2 && temp->prev != NULL)
   {
      i++;
      temp = temp->prev;
   }
   edittop = temp;

   while (lines <= editwinrows - 1 && lines <= totlines && temp != NULL && temp != filebot)
   {
      mvwaddstr(edit, lines, 0, temp->data);
      temp = temp->next;
      lines++;
   } 

   if (temp == filebot)
   {
      mvwaddstr(edit, lines, 0, filebot->data);
      lines++;
      for (i = lines; i <= editwinrows - 1; i++)
         for(j = 0; j <= COLS - 1; j++)
            mvwaddch(edit, i, j, ' ');

   }
   editbot = temp;

}

void do_first_line(void)
{
   current = fileage;
   placewewant = 0;
   current_x = 0;
   edit_update(current);
}

void do_last_line(void)
{
   current = filebot;
   placewewant = 0;
   current_x = 0;
   edit_update(current);
}

/*
 * Ask a question on the statusbar.  Answer will be stored in answer
 * global.  Returns -1 on aborted enter, the valid shortcut key caught, 0
 * otherwise.  Def is any editable text we want to put up by default.
 */
int statusq(shortcut s[], int slen, char *def, char *msg, ...)
{
   va_list ap;
   char foo[133];
   int ret;

   bottombars(s, slen); 

   va_start(ap, msg);
   vsnprintf(foo, 132, msg, ap);
   strncat(foo, ": ", 132);
   va_end(ap);

   wattron(bottomwin, A_REVERSE);
   ret = tipgetstr(foo, def, s, slen, (strlen(foo) + 3));
   wattroff(bottomwin, A_REVERSE);


   switch (ret)
   {

      case TIP_FIRSTLINE_KEY:
         do_first_line();
         break;
      case TIP_LASTLINE_KEY:
         do_last_line();
         break;
   }

   /* Then blank the screen */
   blank_statusbar_refresh();

#ifdef DEBUG
   fprintf(stderr, "I got \"%s\"\n", answer);
#endif

   return ret;
}

/*
 * Ask a simple yes/no question on the statusbar.  Returns 1 for Y, 0 for
 * N, 2 for All (if all is non-zero when passed in) and -1 for abort (^C)
 */
int do_yesno(int all, char *msg, ...)
{
   va_list ap;
   char foo[133];
   int kbinput, ok = -1;

   /* Write the bottom of the screen */
   clear_bottomwin();
   wattron(bottomwin, A_REVERSE);
   blank_statusbar_refresh();
   wattroff(bottomwin, A_REVERSE);

   wmove(bottomwin, 1, 0);
   onekey(" Y", "Yes");
   if (all)
      onekey(" A", "All");
   wmove(bottomwin, 2, 0);
   onekey(" N", "No");
   onekey("^C", "Cancel");
   
   va_start(ap, msg);
   vsnprintf(foo, 132, msg, ap);
   va_end(ap);
   wattron(bottomwin, A_REVERSE);
   mvwaddstr(bottomwin, 0, 0, foo);
   wattroff(bottomwin, A_REVERSE);
   wrefresh(bottomwin);

   reset_cursor();
   raw();

   while (ok == -1)
   {
      kbinput = wgetch(edit);

      switch (kbinput)
      {
         case 'Y': case 'y':
            ok = 1;
            break;
         case 'N': case 'n':
            ok = 0;
            break;
         case 'A': case 'a':
            if (all)
               ok = 2;
            break;
         case TIP_CONTROL_C:
            ok = -2;
            break;
      }
   }
   noraw();
   cbreak();

   /* Then blank the screen */
   blank_statusbar_refresh();

   if (ok == -2)
      return -1;
   else
      return ok;
}

void statusbar(char *msg, ...)
{
   va_list ap;
   char foo[133];
   int start_x = 0;

   va_start(ap, msg);
   vsnprintf(foo, 132, msg, ap);
   va_end(ap);

   start_x = center_x - strlen(foo) / 2 - 1;

   /* Blank out line */
   blank_statusbar_refresh();

   wmove(bottomwin, 0, start_x);
   wattron(bottomwin, A_REVERSE);

   waddstr(bottomwin, "[ ");
   waddstr(bottomwin, foo);
   waddstr(bottomwin, " ]");
   wattroff(bottomwin, A_REVERSE);
   wrefresh(bottomwin);

   statblank = 25;
}

void total_refresh(void)
{
   int i, j;

   redrawwin(edit);
   redrawwin(topwin);
   redrawwin(bottomwin);
   bottombars(main_list, MAIN_LIST_LEN);
   titlebar();
   for (i = 0 ; i <= LINES - 1; i++);
      for (j = i; j != COLS; j++)
         mvwaddch(edit, i, j, ' ');
   wrefresh(edit);

   edit_refresh();
   reset_cursor();
   wrefresh(edit);
   wrefresh(topwin);
   wrefresh(bottomwin);
}

void previous_line(void)
{
   if (current_y > 0)
      current_y--;
   else
      edit_refresh();

   reset_cursor();
}

/* Dump the current file structure to stderr */
void dump_buffer (filestruct *inptr)
{
#ifdef DEBUG
   filestruct *fileptr;

   if (inptr == fileage)
      fprintf(stderr, "Dumping file buffer to stderr...\n");
   else if (inptr == cutbuffer)
      fprintf(stderr, "Dumping cutbuffer to stderr...\n");
   else
      fprintf(stderr, "Dumping a buffer to stderr...\n");

   fileptr = inptr;
   while (fileptr != NULL)
   {
      fprintf(stderr, ">%s", fileptr->data);
      fflush(stderr);
      fileptr = fileptr->next;
   }
#endif /* DEBUG */
}

/* Load file into edit buffer - takes data from file struct */
void load_file(void)
{
   current = fileage;
   wmove(edit, current_y, current_x);
   edit_update(fileage);
   wrefresh(edit);
}

/* Open the file (and decide if it exists) */
void open_file(char *filename)
{
   long size, totsize = 0, linetemp = 0;
   char input[2]; /* buffer */
   char buf[2000] = ""; 
   filestruct *fileptr;

   titlebar();
   fileptr = fileage;

   if (stat(filename, &fileinfo) == -1)	/* We have a new file */
   {
      statusbar("New File");
      fileage = malloc(sizeof(filestruct));
      fileage->data = malloc(2);
      strcpy(fileage->data, "\n");
      fileage->prev = NULL;
      fileage->next = NULL;
      filebot = fileage;
      fileptr = fileage;
      current = fileage;
   }
   else if ((file = open(filename, O_RDONLY)) == -1)
   {
      statusbar("%s: %s", strerror(errno), filename);
   }
   else			/* File is A-OK */
   {
      statusbar("Reading File");

      /* Read the entire file into file struct */
      while ((size = read(file, input, 1)))
      {
         linetemp = 0;
         if (input[0] == '\n')
         {
            if (fileage == NULL)
            {
               fileage = malloc(sizeof(filestruct));
               fileage->data = malloc(strlen(buf)+2);
               strcpy(fileage->data, buf);
               strcat(fileage->data, "\n");
               fileage->prev = NULL;
               fileage->next = NULL;
               filebot = fileage;
               fileptr = fileage;
            }
            else
            {
               filebot->next = malloc(sizeof(filestruct));
               filebot->next->data = malloc(strlen(buf)+2);
               strcpy(filebot->next->data, buf);
               strcat(filebot->next->data, "\n");
               filebot->next->prev = filebot;
               filebot->next->next = NULL;
               filebot = filebot->next;
            }
            totlines++;
            strcpy(buf, "\0");
         }
         else
         {
            strncat(buf, input, 1);
         }

         totsize += size;
      }

#ifdef DEBUG
      fprintf(stderr, "Open_file: read successful - status update\n");
      fflush(stderr);
#endif

      statusbar("Read %d bytes (%d lines)", totsize, totlines);
      wmove(edit, 0, 0);

#ifdef DEBUG
      fprintf(stderr, "Call load_file() begin\n");
#endif
      load_file();
      close(file);

#ifdef DEBUG
      fprintf(stderr, "Call load_file() end\n");
#endif
   }
}

void usage(void)
{
    printf(" Usage: tip -[vwz] +LINE <file>\n");
    printf(" -v: Print version information and exit\n");
    printf(" -w: Don't wrap long lines\n");
    printf(" -z: Enable suspend\n");
    exit(0);
}

void version(void)
{
    printf(" tip version %s by Chris Allegretta\n", VERSION);
}

/* Update cursor location in edit buffer */
void update_cursor(void)
{
   int i = 0;

   wmove(edit, current_y, current_x);

#ifdef DEBUG
   fprintf(stderr, "Moved to (%d, %d) in edit buffer\n", current_y,
                   current_x);
#endif

   current = edittop;
   while (i <= current_y - 1 && current->next != NULL)
   {
      current = current->next;
      i++;
   }

#ifdef DEBUG
   fprintf(stderr, "current->data = \"%s\"\n", current->data);
#endif
   wrefresh(edit);

}

void page_down(void)
{
  if (editbot->next != NULL && editbot->next != filebot)
  {
     edit_update(editbot->next);
     center_cursor();
  }
  else if (editbot != filebot)
  {
     edit_update(editbot);
     center_cursor();
  }
  else
     while (current != filebot)
     {
        current = current->next;
        current_y++;
     }

  update_cursor();
}

filestruct *make_new_node(filestruct *prevnode)
{
   filestruct *newnode;

   newnode = malloc(sizeof(filestruct));
   newnode->data = NULL;

   newnode->prev = prevnode;
   newnode->next = NULL;

   return newnode;
}

void add_to_cutbuffer(filestruct *inptr)
{
   filestruct *tmp;

#ifdef DEBUG
   fprintf(stderr, "add_to_cutbuffer called with inptr->data = %s\n", inptr->data);
#endif

   tmp = cutbuffer;
   if (cutbuffer == NULL)
   {
      cutbuffer = inptr;
      inptr->next = NULL;
      inptr->prev = NULL;
      return;
   }
   else
   {
      while(tmp->next != NULL)
         tmp = tmp->next;
   }

   tmp->next = inptr;
   inptr->prev = tmp;
   inptr->next = NULL;
   cutbottom = inptr;
}

void do_cut_text(filestruct *fileptr)
{
   filestruct *tmp;
      
   tmp = fileptr->next;

#ifdef DEBUG
   fprintf(stderr, "do_cut_text called with fileptr->data = %s\n", fileptr->data);
#endif

   if (!keep_cutbuffer)
   {
      free_filestruct(cutbuffer);
      cutbuffer = NULL;
#ifdef DEBUG
      fprintf(stderr, "Blew away cutbuffer =)\n");
#endif
   }

   if (fileptr == fileage)
   {
      if (fileptr->next != NULL)
      {
         fileptr = fileptr->next;
         tmp = fileptr;
         fileage = fileptr;
         add_to_cutbuffer(fileptr->prev);
         fileptr->prev = NULL;
         edit_update(fileage);
      }
      else
      {
         add_to_cutbuffer(fileptr);
         fileage = make_new_node(NULL);
      }
   } 
   else
   {
      (fileptr->prev)->next = fileptr->next;
      if (fileptr->next != NULL)
         (fileptr->next)->prev = fileptr->prev;
      add_to_cutbuffer(fileptr);
   }

   if (tmp != NULL)
      current = tmp;
   else /* FIXME - wrong */
      tmp = make_new_node(tmp);
   
   if (fileptr == edittop)
      edittop = current;

   edit_refresh();
   wrefresh(edit);

   dump_buffer(cutbuffer);
   reset_cursor();

   keep_cutbuffer = 1;
}

void do_uncut_text(filestruct *fileptr)
{
   filestruct *tmp = fileptr, *newbuf, *newend;

#ifdef DEBUG
   fprintf(stderr, "do_uncut_text called with fileptr->data = %s\n", fileptr->data);
#endif      

   if (cutbuffer == NULL || fileptr == NULL)
      return;	/* AIEEEEEEEEEEEE */

   newbuf = copy_filestruct(cutbuffer);
   /* Make newend = last element in newbuf */
   for (newend = newbuf; newend->next != NULL && newend != NULL; 
           newend = newend->next)
      ;

   /* Hook newbuf into fileptr */
   if (fileptr != fileage)
   {
      tmp = fileptr->prev;
      tmp->next = newbuf;
      newbuf->prev = tmp;
   }
   else
      fileage = newbuf;

   /* Connect the end of the buffer to the filestruct */
   newend->next = fileptr;
   fileptr->prev = newend;
   edit_update(current);
   reset_cursor();
   wrefresh(edit);

   dump_buffer(cutbuffer);
   dump_buffer(fileage);
}

void do_early_abort(void)
{
   blank_statusbar_refresh();
   bottombars(main_list, MAIN_LIST_LEN);
   reset_cursor();
}

/* Set up the system variables for a search or replace.  Returns -1 on
   abort, 0 on success, and 1 on rerun calling program */
int search_init(void)
{
   int i;

   if (strcmp(last_search, ""))	/* There's a previous search stored */
   {
      if (case_sensitive)
         i = statusq(whereis_list, WHEREIS_LIST_LEN, "", 
                     "Case Sensitive Search [%s]", last_search);
      else
         i = statusq(whereis_list, WHEREIS_LIST_LEN, "", "Search [%s]", 
                     last_search);

      if (i == -1) /* Aborted enter */
         strncpy(answer, last_search, 132);
      else if (i == 0) /* They actually entered something */
      {
         strncpy(last_search, answer, 132);

         /* Blow away last_replace because they entered a new search
            string....uh, right? =) */
         strcpy(last_replace, "");
      }
      else if (i == TIP_CASE_KEY) /* They asked for case sensitivity */
      {
         case_sensitive = 1 - case_sensitive;
         return 1;
      }
      else /* First page, last page, for example could get here */
      {
         do_early_abort();
         return -1;
      }
   }
   else /* last_search is empty */
   {
      if (case_sensitive)
         i = statusq(whereis_list, WHEREIS_LIST_LEN, "",
                     "Case Sensititve Search");
      else
         i = statusq(whereis_list, WHEREIS_LIST_LEN, "", "Search");
      if (i == -1)
      {
         statusbar("Aborted");
         reset_cursor();
         return -1;
      }
      else if (i == 0) /* They entered something new */
         strncpy(last_search, answer, 132);
      else if (i == TIP_CASE_KEY) /* They want it case sensitive */
      {
         case_sensitive = 1 - case_sensitive;
         return 1;
      }
      else /* First line key, etc. */
      {
         do_early_abort();
         return -1;
      }
   }

   return 0;
}
filestruct *findnextstr(int quiet, filestruct *begin, char *needle)
{
   filestruct *fileptr;
   char *searchstr, *found, *tmp;

   fileptr = current;

   searchstr = &current->data[current_x+1]; 
   /* Look for searchstr until EOF */
   while (fileptr != NULL && 
         (found = strstrwrapper(searchstr, needle)) == NULL)
   {
       fileptr = fileptr->next;

      if (fileptr == begin)
         return NULL;

      if (fileptr != NULL)
         searchstr = fileptr->data;
   }

   /* If we're not at EOF, we found an instance */
   if (fileptr != NULL)
   {
      current = fileptr;
      current_x = 0;
      for (tmp = fileptr->data; tmp != found; tmp++)
         current_x++;

      edit_update(current);
      reset_cursor();
   }
   else	/* We're at EOF, go back to the top, once */
   {
      fileptr = fileage;

      while(fileptr != current && fileptr != begin && 
            (found = strstrwrapper(fileptr->data,  needle)) == NULL)
         fileptr = fileptr->next;

      if (fileptr == begin)
         return NULL;

      if (fileptr != current)	/* We found something */
      {
         current = fileptr;
         current_x = 0;
         for (tmp = fileptr->data; tmp != found; tmp++)
            current_x++;

         edit_update(current);
         reset_cursor();

         if (!quiet)
            statusbar("Search Wrapped");
      }
      else	/* Nada */
      {
         if (!quiet)
            statusbar("Search string not found");
         return NULL;
      }
   }

   return fileptr;
}

/* Search for a string */
void do_search(void)
{
   int i;

   if ((i = search_init()) == -1)
      return;
   else if (i == 1)
   {
      do_search();
      return;
   }

   findnextstr(0, current, answer);
}

void print_replaced(int num)
{
   if (num > 1)
      statusbar("Replaced %d occurences", num);
   else if (num == 1)
      statusbar("Replaced 1 occurence");
}

/* Search for a string */
void do_replace (void)
{
   int i, j, replaceall = 0, numreplaced = 0, beginx;
   filestruct *fileptr, *begin;
   char *tmp, *copy, prevanswer[132] = "";

   if ((i = search_init()) == -1)
      return;
   else if (i == 1)
   {
      do_replace();
      return;
   }

   strncpy(prevanswer, answer, 132);

   if (strcmp(last_replace, ""))	/* There's a previous replace str */
   {
      i = statusq(replace_list, REPLACE_LIST_LEN, "", 
                     "Replace with [%s]", last_replace);

      if (i == -1) /* Aborted enter */
         strncpy(answer, last_replace, 132);
      else if (i == 0) /* They actually entered something */
         strncpy(last_replace, answer, 132);
      else if (i == TIP_CASE_KEY) /* They asked for case sensitivity */
      {
         case_sensitive = 1 - case_sensitive;
         do_replace();
         return;
      }
      else /* First page, last page, for example could get here */
      {
         do_early_abort();
         return;
      }
   }
   else /* last_search is empty */
   {
      i = statusq(replace_list, REPLACE_LIST_LEN, "", "Replace with");
      if (i == -1)
      {
         statusbar("Aborted");
         reset_cursor();
         return;
      }
      else if (i == 0) /* They entered something new */
         strncpy(last_replace, answer, 132);
      else if (i == TIP_CASE_KEY) /* They want it case sensitive */
      {
         case_sensitive = 1 - case_sensitive;
         do_replace();
         return;
      }
      else /* First line key, etc. */
      {
         do_early_abort();
         return;
      }
   }
   
   begin = current;
   beginx = current_x;
   while (1)
   {

      if (replaceall)
         fileptr = findnextstr(1, begin, prevanswer);
      else 
         fileptr = findnextstr(0, begin, prevanswer);

      if (fileptr == NULL)
      {
         current = begin;
         current_x = beginx;
         edit_update(current);
         print_replaced(numreplaced);
         return;
      }
   
      /* If we're here, we've found the search string */
      if (!replaceall)
         i = do_yesno(1, "Replace this instance?");

      if (i == 1 || replaceall) /* Yes, replace it!!!! */
      {

         /* FIXME - lots of ugly code */
         copy = malloc(strlen(current->data) - strlen(last_search) + 
                       strlen(last_replace) + 1);

         strncpy(copy, current->data, current_x);
         copy[current_x] = 0;

         strcat(copy, last_replace);

         for (j = 1, tmp = current->data; j <= 
             (strlen(last_search) + current_x) && *tmp != 0; j++)
            tmp++;

         if (*tmp != 0)
            strcat(copy, tmp);

         tmp = current->data;
         current->data = copy;

         free(tmp);

         edit_refresh();

         if (!modified)
         {
            modified = 1;
            titlebar();
         }
         numreplaced++;
      }
      else if (i == 2) /* replace all, aieeeeeeeeeeeeee */
         replaceall = 1;
      else if (i == -1) /* Abort, else do nothing and continue loop */
         break;
      }

   print_replaced(numreplaced);
}


/* What happens when we want to go past the bottom of the buffer */
void do_down(void)
{
   if (current->next != NULL)
   {
      if (placewewant > 0)
         current_x = placewewant;

      if (current_x > strlen(current->next->data) - 1)
         current_x = strlen(current->next->data) - 1;
   }
   
   if (current_y < editwineob && current != editbot)
      current_y++;
   else
      page_down();

  wrefresh(edit);
}

void page_up(void)
{
   if (edittop != fileage)
   {
      edit_update(edittop);
      center_cursor();
   }
   else
      current_y = 0;

   update_cursor();
}

void do_up(void)
{
   if (current->prev != NULL)
   {
      if (placewewant > 0)
         current_x = placewewant;

      if (current_x > strlen(current->prev->data) - 1)
         current_x = strlen(current->prev->data) - 1;
   }

   if (current_y > 0)
      current_y--;
   else
      page_up();

  wrefresh(edit);
}

void do_right(void)
{
   if (current_x < strlen(current->data) - 1)
      current_x++;
   else
   {
      current_x = 0;
      placewewant = 0;
      do_down();
   }

   placewewant = current_x;
}

void do_left(void)
{
   if (current_x > 0)
      current_x--;
   else if (current != fileage)
   {
      current_x = strlen(current->prev->data) - 1;
      placewewant = 0;
      do_up();
   }
   else
      statusbar("Beep!");

   placewewant = current_x;
}

void delete_buffer(filestruct *inptr)
{
   if (inptr != NULL)
   {
      delete_buffer(inptr->next);
      free(inptr->data);
      free(inptr);
   }
}

void do_backspace(void)
{
   filestruct *previous;

   if (current_x != 0)
   {
      /* Let's get dangerous */
      memmove(&current->data[current_x - 1], &current->data[current_x], 
              strlen(current->data) - current_x + 2);
#ifdef DEBUG
     fprintf(stderr, "current->data now = \"%s\"\n", current->data);
#endif 
      current->data = realloc(current->data, strlen(current->data) + 1);
      current_x--;
   }
   else
   {
      if (current == fileage)
         return;	/* Can't delete past top of file */

      previous = current->prev;
      current_x = strlen(previous->data) - 1;
      previous->data = realloc(previous->data,
                       strlen(previous->data) + strlen(current->data) + 2);
      strip_newline(previous->data);
      strcat(previous->data, current->data);

      unlink_node(current);
      delete_node(current);
      if (current == edittop)
         page_up();
      current = previous;
      previous_line();
      wrefresh(edit);

#ifdef DEBUG
      fprintf(stderr, "After, data = \"%s\"\n", current->data);
#endif

   }
   if (!modified)
   {
      modified = 1;
      titlebar();
   }

   edit_refresh();
   update_cursor();
   wrefresh(edit);
   keep_cutbuffer = 0;
}

/* Someone hits return *gasp!*  - basically a stripped down version of
   do_wrap() =-) */
void do_enter(filestruct *inptr)
{
   filestruct *new;
   char *tmp;

   new = make_new_node(inptr);

   tmp = &current->data[current_x];
   new->data = malloc(strlen(tmp) + 2);
   strcpy(new->data, tmp);
   *tmp++ = '\n';
   *tmp = 0;

   new->next = inptr->next;
   inptr->next = new;
   new->next->prev = new;

   current = new;
   current_x = 0;

   inptr->data = realloc(inptr->data, strlen(inptr->data) + 2);  

   if (current_y == editwinrows - 1)
      edit_update(current);
   else
      edit_refresh();

   reset_cursor();
   wrefresh(edit);
   totlines++;

}

/* Actually wrap a line, called by check_wrap() */
void do_wrap(filestruct *inptr)
{
   filestruct *new;
   char *tmp, *foo;
   int backup = 0, jumptonext = 0;

   new = make_new_node(inptr);

   tmp = inptr->data + COLS - 1;
   while (tmp != inptr->data && *tmp == ' ')
   {
      tmp--;
      backup++;
   }
   while (tmp != inptr->data && *tmp != ' ')
   {
      tmp--;
      backup++;
   }

   if (backup > COLS - current_x)
      jumptonext = 1;

   if (tmp == inptr->data)
      return;
   tmp++;

   new->data = malloc(strlen(tmp) + 2);

   strcpy(new->data, tmp);
   *tmp++ = '\n';
   *tmp++ = 0;
   inptr->data = realloc(inptr->data, strlen(inptr->data) + 1);  

   if (inptr->next != NULL && inptr->next->wrapline == 1)
   {
      foo = malloc(strlen(new->data) + strlen(inptr->next->data) + 2);
      strcpy(foo, new->data);
      strip_newline(foo);
      strcat(foo, inptr->next->data);
      inptr->next->data = foo;

      free(new);
   }
   else
   {
      fflush(stderr);

      new->next = inptr->next;
      inptr->next = new;
      new->next->prev = new;
      new->wrapline = 1;
   }

   if (jumptonext == 1)
   {
      current = inptr->next;
      current_x = backup - (COLS - 1 - current_x);
   }
   else if (current_x == COLS - 1)
   {
      current = inptr->next;
      current_x = strlen(new->data)-1;
   }
   
   edit_refresh();
   reset_cursor();
   wrefresh(edit);
   totlines++;

}

/* Check to see if we've just caused the line to wrap to a new line */
void check_wrap(filestruct *inptr)
{
   if ((int) strlen(inptr->data) <= COLS)
      return;
   else
      do_wrap(inptr);
}

void do_gotoline(void)
{
   long line, i = 1, j = 0;
   filestruct *fileptr;

   j = statusq(replace_list, REPLACE_LIST_LEN, "", "Enter line number");
   if (j == -1)
   {
      statusbar("Aborted");
      reset_cursor();
      return;
   }
   else if (j != 0)
   {
      do_early_abort();
      return;
   }

   if (!strcmp(answer, "$"))
   {
      current = filebot;
      current_x = 0;
      edit_update(current);
      reset_cursor();
      return;
   }

   line = atoi(answer);
   /* Bounds check */
   if (line <= 0)
   {
      statusbar("Come on, be reasonable");
      return;
   }

   if (line > totlines) /* FIXME - make totlines update when a new line is
			   added / lines are uncut */
   {
      statusbar("Only %d lines available, skipping to last line", totlines);
      current = filebot;
      current_x = 0;
      edit_update(current);
      reset_cursor();
   }
   else
   {
      for (fileptr = fileage; fileptr != NULL && i < line; i++)
         fileptr = fileptr->next;

      current = fileptr;
      current_x = 0;
      edit_update(current);
      reset_cursor();
   }   

}

void wrap_reset(void)
{
   if (current != NULL)
      current->wrapline = 0;
   else
      return;

   if (current->next != NULL)
      current->next->wrapline = 0;
}

int write_file(char *name)
{
   long size, totsize = 0, linetemp = 0, lineswritten = 0;
   char input[2]; /* buffer */
   filestruct *fileptr;

   titlebar();
   fileptr = fileage;

   if ((file = open(name, O_WRONLY | O_CREAT | O_TRUNC)) == -1)
   {
      statusbar("Could not open file for writing: %s", strerror(errno));
      return -1;
   }

      dump_buffer(fileage);
      /* Read the entire file into file struct */
      while (fileptr != NULL)
      {
         size = write(file, fileptr->data, strlen(fileptr->data));
         if (size == -1)
         {
            statusbar("Could not open file for writing: %s",
                      strerror(errno));
            return -1;
         }
         else
         {
#ifdef DEBUG
            fprintf(stderr, "Wrote >%s", fileptr->data);
#endif
         }
         fileptr = fileptr->next;
         lineswritten++;
      }

   statusbar("Wrote %d lines", lineswritten);
   return 0;
}

void do_writeout(void)
{
   int i;

   i = statusq(writefile_list, WRITEFILE_LIST_LEN, filename, 
                  "File Name to write");
   if (i != -1)
   {

#ifdef DEBUG
      fprintf(stderr, "filename is %s", answer);     
#endif

      i = write_file(answer);
   }

   return;
}


void do_exit(void)
{
   int i;

   if (!modified)
      finish(0);

   i = do_yesno(0, "Save modified buffer (ANSWERING \"No\" WILL DESTROY CHANGES) ?");

   if (i == 1)
      do_writeout();

   if (i != -1) 
      finish(0);

}

int main(int argc, char *argv[])
{
    char optchr;
    int kbinput;			/* Input from keyboard */

    while ((optchr = getopt(argc, argv, "h?vz")) != EOF) {
	switch (optchr) {
	case 'h':
	case '?':
	    usage();
	case 'v':
	    version();
	    exit(0);
        case 'z':
            suspend=1;
            break;
        default:
            usage();
	}
    }

    if (argc == 1)
       usage();

    strncpy(filename, argv[argc - 1], 132);

    initscr();
    savetty();
    nonl();
    cbreak();
    noecho();
    timeout(0);

    signal(SIGINT, SIG_IGN);
    if (!suspend)
       signal(SIGTSTP, SIG_IGN);

    /* Set up some global variables */
    global_init();

#ifdef DEBUG
    fprintf(stderr, "Main: set up windows\n");
#endif

    /* Setup up the main text window */
    edit = newwin(editwinrows, COLS, 2, 0);
    keypad(edit, TRUE);

    /* And the other windows */
    topwin = newwin(2, COLS, 0, 0);
    bottomwin = newwin(3, COLS, LINES - 3, 0);
    keypad(bottomwin, TRUE);

#ifdef DEBUG
    fprintf(stderr, "Main: bottom win\n");
#endif
    /* Set up up bottom of window */
    bottombars(main_list, MAIN_LIST_LEN);

#ifdef DEBUG
    fprintf(stderr, "Main: open file\n");
#endif

    open_file(filename);

    wmove(edit, 0, 0);
    wrefresh(edit);
    
    while (1)
    {
       kbinput = wgetch(edit);
       switch(kbinput)
       {
	case TIP_EXIT_KEY:
          do_exit();
          break;
       case TIP_WRITEOUT_KEY:
          do_writeout();
          bottombars(main_list, MAIN_LIST_LEN);
          break;
       case TIP_GOTO_KEY:
          wrap_reset();
          do_gotoline();
          keep_cutbuffer = 0;
          bottombars(main_list, MAIN_LIST_LEN);
          break;
       case TIP_WHEREIS_KEY:
          wrap_reset();
          do_search();
          keep_cutbuffer = 0;
          bottombars(main_list, MAIN_LIST_LEN);
          wrefresh(bottomwin);
          break;
       case TIP_CUT_KEY:
          do_cut_text(current);
          break;
       case 1:		/* ^A */
          current_x = 0;
          placewewant = 0;
          break;
       case TIP_INSERTFILE_KEY:
          wrap_reset();
#ifdef DEBUG
	  fprintf(stderr, "Insert file - not yet implemented\n");
#endif
          keep_cutbuffer = 0;
          break;
       case TIP_PREVPAGE_KEY:
          wrap_reset();
          current_x = 0;
          page_up();
          keep_cutbuffer = 0;
          check_statblank();          
          break;
       case TIP_NEXTPAGE_KEY:
          wrap_reset();
          current_x = 0;
          page_down();
          keep_cutbuffer = 0;
          check_statblank();          
          break;
       case TIP_UNCUT_KEY:
          wrap_reset();
          do_uncut_text(current);
          keep_cutbuffer = 0;
          break;
       case TIP_SPELL_KEY:
#ifdef DEBUG
	  fprintf(stderr, "To Spell - not yet implemented\n");
#endif
          keep_cutbuffer = 0;
          break;
       case TIP_REPLACE_KEY:
          do_replace();
          keep_cutbuffer = 0;
          bottombars(main_list, MAIN_LIST_LEN);
          break;
       case KEY_UP:
          wrap_reset();
          do_up();
          update_cursor();
          keep_cutbuffer = 0;
          check_statblank();          
          break;
       case KEY_DOWN:
          wrap_reset();
          do_down();
          update_cursor();
          keep_cutbuffer = 0;
          check_statblank();          
          break;
       case KEY_LEFT:
          do_left();
          update_cursor();
          keep_cutbuffer = 0;
          check_statblank();          
          break;
       case KEY_RIGHT:
          do_right();
          update_cursor();
          keep_cutbuffer = 0;
          check_statblank();          
          break;
       case KEY_BACKSPACE: case KEY_DC: case 127:
          do_backspace();
          break;
       case TIP_REFRESH_KEY:
          total_refresh();
          break;
       case 13:		/* Enter (^M) - FIXME - must be more things 
                           bound to enter key */
          do_enter(current);
          break;
       default:
          /* More dangerousness fun =) */
          current->data = realloc(current->data, strlen(current->data) + 2);
          memmove(&current->data[current_x+1], &current->data[current_x], 
                    strlen(current->data) - current_x + 1);
          current->data[current_x] = kbinput;
          update_line(current); 
          do_right();
          update_cursor();
          check_wrap(current); 
          wrefresh(edit);
          if (!modified)
          {
             modified = 1;
             titlebar();
          }
          check_statblank();          
          keep_cutbuffer = 0;
       }
       reset_cursor();

    }

    getchar();
    finish(0);

}
