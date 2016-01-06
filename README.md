# latex-wordcount

## Credit / License
Basic part of the script is from Stuart Curtis - [latexwordcount](http://sourceforge.net/projects/latexwordcount/).

It is therefore under the same license:

	This code is released under the GPLv2 license allowing its free use, modification and distribution.

See the [license file](latex-wordcount/raw/master/gpl-2.0.txt) for more information.

## Purpose
Counts number of words in a LaTeX file.

Either just run the script with a *tex*-file as argument:

    python wordcount.py file.tex

Or use the class in another python script:	

```python	
	from wordcount import LatexWordCounter
	counter = LatexWordCounter(["file.tex"])
	print counter.count_words() # returns number of words in file.tex
```

You can also add whole folders containing several .tex files:

```python	
	from wordcount import LatexWordCounter
	counter = LatexWordCounter(["file.tex"])
	counter.add_folder("chapters")
	print counter.count_words() # returns number of words in file.tex+all .tex files in chapters/
```

## Word count
Counted as text:

* normal text
* headers

Not counted as words:

* references (*\ref*, *\cite*)
* header, footer


## Known Bugs
* Doesn't count word if adjacent to backslash (*word\normalsize* is not counted)
* Bold, italic and underlined words are not counted (*\textbf{word}* is not counted)
* Counts commands that begin '{\' as words
* Raises error if $ and $$ occur in a single word
