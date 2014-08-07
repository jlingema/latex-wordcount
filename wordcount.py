#!/usr/local/bin/python
# -*- coding: utf-8 -*-
#
# Counts number of words in a LaTeX file.
#
# Some changes by Adrianus Kleemans
# Changed into a class structure by Joschka Lingemann
# modified 07.08.2014
# Original script by Stuart Curtis
#

import os
import sys

class LatexWordCounter(object):
    """A class that is able to read latex files and counts number of words"""
    def __init__(self, files = None):
        super(LatexWordCounter, self).__init__()
        self._files = []
        if files != None:
            self._files = files
        self.n_words = 0
        self._prepared = False
        self._words = []
        self.word_numbers = [0]
        self.ignoredList = ["document", "tiny", "scriptsize", "footnotesize", "small", "normalsize", "large", "Large", "LARGE", "huge", "huge", "flushleft", "center", "flushright"]
        
    def add_file(self, fname):
        self._files.append(fname)
    
    def add_folder(self, path):
        for r, dirs, files in os.walk(path):
            self._files += [ "{dir}/{fname}".format(dir=r, fname=f) for f in files if ".tex" in f]

    def prepare(self):
        # read all files
        lines = []
        for fname in self._files:
            try:
                f = open(fname, 'rb')
            except IOError:
                print fname
                print("Please provide a valid .tex-file.")
                sys.exit()        
            wholewords = f.read()
            f.close()
            lines += wholewords.splitlines()

        i = 0
        # remove comments
        while i < len(lines):
            if len(lines[i]) > 0 and lines[i][0] == "%":
                del(lines[i])
                continue
            if lines[i].find("%") != -1:
                if lines[i][lines[i].find("%")-1] != ("\\"):
                    lines[i] = lines[i][:lines[i].find("%")]
            if len(lines[i]) == 0:
                lines.pop(i)
                continue
            i +=1
        self._words = []
        for i in range(len(lines)):
                self._words.append(lines[i].split())
        self._words = sum(self._words, [])

    
    def count_words(self):
        self.prepare()
        self.word_numbers = range(len(self._words))
        for i in range(len(self._words)):
            # "dollar sign" equations
            if self._words[i].count("$")>0 and self._words[i].count("$")%2 == 0 and self._words[i].count("$$")%2 == 0:
                try: 
                    self.word_numbers.remove(i)
                except ValueError:
                    continue                
            elif self._words[i].count("$")%2 == 1 and self._words[i].count("$$")%2 == 0 and self.word_numbers.count(i) == 1:
                self.word_numbers.remove(i)
                self.dollar(i+1, self._words[i].count("$"), 1)
            elif self._words[i].count("$")%2 == 0 and self._words[i].count("$$")%2 == 1 and self.word_numbers.count(i) == 1:
                self.word_numbers.remove(i)
                self.dollar(i+1, self._words[i].count("$$"), 2)
            #begin and end functions
            elif self._words[i].find("\\begin{") == 0:
                self.begin(self._words[i][7:self._words[i].find("}")], i)
            elif self._words[i].find("\\begin{") > 0:
                self.begin(self._words[i][7:self._words[i].find("}")], i+1)
            #named functions
            elif self._words[i].find("\\") == 0 and self._words[i].count("{") == self._words[i].count("}") and self._words[i].count("[") == self._words[i].count("]"):
                try: 
                    self.word_numbers.remove(i)
                except ValueError:
                    continue
            elif self._words[i].find("\\") == 0 and self._words[i].count("{") > self._words[i].count("}") or self._words[i].count("[") > self._words[i].count("]"):
                try: 
                    self.word_numbers.remove(i)
                except ValueError:
                    continue
                self.backslashFn(i+1, self._words[i].count("{"), self._words[i].count("}"), self._words[i].count("["), self._words[i].count("]"))

            return len(self.word_numbers)

    def begin(self, command, index):
            i = index
            if self.ignoredList.count(command):
                try: self.word_numbers.remove(i)
                except ValueError:
                    return
                        
                while self._words[i].find("\\end{" + str(command) +"}") == -1:
                        i+=1
                try: self.word_numbers.remove(i)
                except ValueError:
                    return
            else:
                    while self._words[i].find("\\end{" + str(command) +"}") == -1:
                        try: self.word_numbers.remove(i)
                        except ValueError:
                                return
                        i+=1
                    self.word_numbers.remove(i)
                    return        

    def backslashFn(self, index, opnCu, clsCu, opnSq, clsSq):
            try: self.word_numbers.remove(index)
            except ValueError:
                return
            opnCu += self._words[index].count("{")
            clsCu += self._words[index].count("}")
            opnSq += self._words[index].count("[")
            clsSq += self._words[index].count("]")
            if clsCu == opnCu and clsSq == opnSq:
                return
            else:
                return self.backslashFn(index+1, opnCu, clsCu, opnSq, clsSq)     

    def dollar(self, index, no, sinDbl):
            #print index, no
            try: self.word_numbers.remove(index)
            except ValueError:
                return
            no += self._words[index].count("$"*sinDbl)
            if no%2 == 0:
                return
            else:
                return self.dollar(index+1, no, sinDbl)


# read command line argument
if __name__ == "__main__":
    try:
        path = sys.argv[1]
    except IndexError:
        print("Please provide a file name for counting.")
        sys.exit()

    counter = LatexWordCounter([path])
    n = counter.count_words()
    print("{} words".format(n))
