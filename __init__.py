#! python
''' See https://rivtDocs.net  for user manual

Introduction
============

rivt is an open source Python package that processes a new plain text markup
language - rivttext. rivttext was designed to write engineering documents that
can be shared as easily modified templates. rivt runs on any platform that
supports Python 3.8 or later and prioritizes simplicity, flexibility,
efficiency and universal access.

The rivt api wraps and extends the Github (gfm) and reStructuredText (reST)
markup languages defined at https://docutils.sourceforge.io/rst.html and xxx. 

A rivt file begins with the import statement:

*import rivt.rivtapi as rv*
 
which provides four API functions:
    
rv.R(rmS) - repository and report information (Repo)
rv.I(rmS) - static text, images, tables and math (Insert)
rv.V(rmS) - equations (Values)
rv.T(rmS) - Python functions and scripts (Tools)

A rivt document is made up of an arbitrary sequence of the three later string
methods following the initial method rv.R. Each method takes a single literal
(triple) string argument referred to as a rivt method string (rms) or rivt
string. When running in an IDE (e.g. VSCode), each method may be run
interactively using the standard cell decorator (# %%). The rv.writedoc() and
rv.reportdoc() functions generate documents and compilations in GitHub Markdown
(ghmd) and PDF formats. Interactive output to the terminal and VSCode
interative window is utf-8.

rivt works for both simple short documents and extensive reports. The rivt
folder structure shown below is designed to support both. A rivt project
includes public folders; *rivt-*report-label and *private* folders intended
for client and other confidential or proprietary files and information. 

Output files are written in two places, depending on the output type.
The Markdown output is written to a README.md file within the public *rivt-*
subfolder and may be read, searched and shared on version control platforms
like GitHub. Private information is not written to the README. The PDF output
is written to the doc folder in *private*.

Folder and file name prefixes that are fixed are shown in [ ] in the example
below. Folder labels may be combinations of specified prefixes and user labels.


Example Folder Structure (required prefixes shown in [])
=========================================================

[rivt-doc]-Report-Label/               
    ├── .git
    ├── units.py                        (unit over-ride)
    ├── README.md                       (output toc and summary)                                      
    ├── rivt1.ini                       (config file)
    ├── [div01]-div-label/                  (division label)
        ├── [doc01]-doc-label/                  (doc label)
            ├── [data0101]/                         (resource data)
                ├── data1.csv                   
                ├── paper1.pdf
                └── functions1.py                   
            ├── [rivt]-file-name.py                 (rivt file)
            └── README.md                           (output doc)
        ├── [doc02]-doc-label/                  (doc label)
            ├── data[0102]/                         (resourde data)
                ├── data1.csv
                ├── fig1.png
                └── fig2.png
            ├── [rivt]-file-name.py                 (rivt file)
            └── README.md                           (output doc)
    ├── [div02]-div-label/                  (division label)
        ├── [doc01]-doc-label/                  (doc label)
            ├── [data0201]/                         (resource data)                   
                ├── data1.csv
                ├── attachment.pdf
                ├── functions.py
                └── fig1.png
            ├── [rivt]-file-name.py                 (rivt file)   
            └── README.md                           (output doc)
    └── [private]/                          (private files)
        ├── [temp]/                         (temp output files)
        ├── [report]/                       (report files)
            ├── r0101-Doc-Label1.pdf        (output docs)
            ├── r0102-Doc-Label2.pdf
            ├── r0201-Doc-Label3.pdf
            └── Report-Label.pdf                (compiled PDF report)    
        ├── images/                             (optional data folders ...)
            ├── fig1.png
            └── fig2.png
        ├── text/    
            ├── text1.txt
            └── text2.txt
        ├── append/    
            ├── report1.pdf
            └── report2.pdf
        └── tables/
            ├── data1.csv
            └── data1.xls


The API is designed for sharing files in the *rivt-* folder. Files in this
folder include the core information in the document - the text, equations,
functions and tables. Files in the *private-* folder are typically not shared.
This two-part folder and file structure simplifies protection of confidential
content, while applying version control and sharing for the primary calculation
inputs.

Commands and Tags
=================

rivt syntax includes arbitrary unicode text with rivt commands and tags. Syntax
is interepreted within the rivt methods. A rivt command reads or writes
external files and is denoted by || at the beginning of a line. Command
parameters are separated by |. In the summary below parameter options
desginated with semi-colons and list parameters with commas. 

Tags format a line or block of text and are denoted with _[tag] at the end of a
line. Block tags start a block of text with _[[tag]] and end with _[[q]]. The
"=" and ":=" tags used in the Value method are the exceptions.

The first line of each method is a section label followed by section
parameters. Section labels may be omitted by prepending with a double hyphen --.

======= ===================================================================
 name             API Functions and commands (VSCode snippet prefix)
======= ===================================================================

Repo    rv.R("""label | toc; notoc | page
(re)
                ||text (tex)
                ||append (app)

                """)

Insert  rv.I("""label | rgb; default
(in)
                ||image (img)
                ||text (tex)
                ||table (tab)

                """)

Values  rv.V("""label | sub; nosub 
(va)
                ||declare (dec)

                """)

Tools  rv.T("""label | rgb; default; noprint 
(to)
                Python code

                """)

exclude rv.X("""any method

                Any method changed to X is not evaluated. It may be used for
                comments and debugging.

                """)

write   rv.writedoc('md,utf,pdf')
(wr)
=============================================================== ============
    command syntax and description (snippet)                         API 
=============================================================== ============

|| init | rel file path                                               R
    (ini)   config file path

|| append | rel file path                                             R
    (app)   pdf path

|| text | rel file path | text type                                 R I V
    (tex)   .txt | plain; tags

|| image  | rel file path | .50, ..                                 R I V
    (img)   .png; .jpg |  page width 

|| table  | rel file path | 60,r;l;c                                R I V
    (tab)   .csv; xls  | max col width, align

|| declare | rel file path | print,;noprint                           V
    (dec)    .csv; .xls  | print or hide

============================ ============================================
 tags                                  description 
============================ ============================================
single lines in R,I,V:
text _[b]                       bold 
text _[c]                       center
text _[i]                       italic
text _[bc]                      bold center 
text _[bi]                      bold italic
text _[r]                       right justify
text _[u]                       underline   
text _[l]                       LaTeX math
text _[s]                       sympy math
text _[bs]                      bold sympy math
text _[e]                       equation label and autonumber
text _[f]                       figure caption and autonumber
text _[t]                       table title and autonumber
text _[#]                       footnote and autonumber
text _[d]                       footnote description 
_[page]                         new page
_[address, label]               url or internal reference

single lines in V: 
a = n | unit, alt | descrip    declare = 
a := b + c | unit, alt | n,n   assign := 

blocks in R,I,V:          
_[[b]]                          bold
_[[c]]                          center
_[[i]]                          italic
_[[p]]                          plain  
_[[l]]                          LaTeX
_[[q]]                          quit block


The first line of a rivt file is *import rivt.rivtapi as rv* followed by
the Repo method rv.R() which occurs once. rv.R is followed by any of the other
three methods in any number or order. rv.R() sets options for repository and
report output.

File format conventions follow the Python formatter pep8, and linter ruff.
Method names start in column one. All other lines must be indented 4 spaces to
facilitate section folding, bookmarks and legibility.

The first line of each rivt method defines the section title and section
parameters. 

============================================================================
rivt example
============================================================================

import rivt.rivtapi as rv

rv.R("""Introduction | white | 1

    The Repo method (short for repository and report) is the first method of a
    rivt doc and specifies document configuration settings.

    The first line of a method is the heading line that starts a new document
    section. If the section heading is preceded by two dashes (--) it becomes a
    section reference and a new section is not started. The color parameter
    applies only to PDF output and specfies the background color for the
    section heading. The page number is the starting page number for the
    doc when processed as a stand alone document.

    The init command specifies the path to the doc configuration file. 

    ||init | config/rivt.ini
    
    The ||text command inserts text from external files into the rivt file.
    Text files may be plain text or text with rivt tags.
    
    ||text | text/describe.txt | rivt 

    The ||table command inserts and formats tabular data from csv or xls files.

    || table | data | file.csv | 60,r
    
    The ||append command attaches PDF files to the end of the doc.

    || append | append/report1.pdf
    || append | append/report2.pdf

    
    """)

rv.I("""The Insert method | green | heading; all

    The Insert method formats static information e.g. images and text.

    The ||text command inserts and formats text from external files into the
    rivt file. Text files may be plain text or text with rivt tags.

    ||text | rel file path | text type    

    The ||table command inserts and formats tabular data from csv or xls files.
    
    The _[t] tag formats and autonumbers table titles.

    A table title  _[t]
    || table | data | file.csv | 60,r

    The ||image command inserts and formats image data from png or jpg files.

    The _[f] tag formats and autonumbers figures.
        
    A figure caption _[f]
    || image | resource | f1.png | 50

    Two images may be placed side by side as follows:

    The first figure caption  _[f]
    The second figure caption  _[f]
    || image | f2.png,f3.png | 45,35
    

    The tags _[x] and _[s] format LaTeX and sympy equations:

    \gamma = \frac{5}{x+y} + 3  _[x] 

    x = 32 + (y/2)  _[s]

    """)

rv.V("""The Values method | white | sub; nosub 

    The Values method assigns values to variables and evaluates equations. The
    sub; nosub setting specifies whether the equations are printed a second
    time with substituted numerical values.

    A table tag provides a table title and number.  
    
    The equal tag declares a value. A sequence of declared values terminated
    with a blank line are formatted as a table.
    
    Example of assignment list _[t]
    f1 = 10.1 * LBF | N | a force
    d1 = 12.1 * IN | CM | a length

    An equation tag provides an equation description and number. A colon-equal
    tag assigns a value and specifies the result units and printed output
    decimal places in the result and equation.

    Example equation - Area of circle  _[e]
    a1 := 3.14(d1/2)^2 | IN^2, CM^2 | 1,2

    || declare | data0102/values0102.csv
    
    The declare command imports values from a csv file written by rivt when
    processing assigned and declared values from another doc in the same
    project.

""")

rv.T("""The Tools method | white | print; noprint 

    # The Tools method processes Python code in the rivt namespace. Functions
    # may be written explicitly or imported from files. All line comments (#) 
    # are printed. Triple quotes cannot be used. The "print" parameter specifies
    whether the code itself is echoed in the document.
    
    # Four Python libraries are imported by rivt and available as: 

    # pyplot -> plt
    # numpy -> np
    # pandas -> pd
    # sympy -> sy
    
    # Examples of Python code:
    # Define a function -
    def f1(x,y): z = x + y
        print(z)
        return Z
    # Read and write files -    
    with open('file.csv', 'r') as f: 
        input = f.readlines()
    
    var = range(10)
    with open('fileout.csv', 'w') as f: 
        f.write(var)
        
    """)

rv.X("""any text

    Replacing a method letter with X skips evaluation of that string. Its
    uses include review comments, checking and editing.

    """) 

============== =========================================================
Keystroke                   VSCode rivt shortcuts and extensions
============== =========================================================

alt+q                rewrap paragraph with hard line feeds (80 default)
alt+p                open file under cursor
alt+.                select correct spelling under cursor
alt+8                insert date
alt+9                insert time

ctl+1                focus on first editor
ctl+2                focus on next editor
ctl+3                focus on previous editor
ctl+8                focus on explorer pane
ctl+9                focus on github pane    

ctl+alt+x            reload window
ctl+alt+u            unfold all code
ctl+alt+f            fold code level 2 (rivt sections visible)
ctl+alt+a            fold code - all levels
ctl+alt+t            toggle local fold
ctl+alt+e            toggle explorer sort order
ctl+alt+s            toggle spell check
ctl+alt+g            next editor group

ctl+shift+u          open URL under cursor in browser
ctl+shift+s          open GitHub rivt README search
ctl+shift+a          commit all 
ctl+shift+z          commit current editor
ctl+shift+x          post to remote   


rivt installation
=================

The minimum software needed to run is:

- Python 3.8 or higher 
- rivt library + Python dependencies

A complete rivt system additionally includes:

- VSCode + extensions 
- LaTeX 
- Github account

rivt-sys installs the complete rivt system in a portable folder via a zip file,
and is available for every OS platform. rivt also runs in the cloud using
GitHub CodeSpaces or other cloud service providers. Installation details are
provided in the [rivt User Manual](https://www.rivt-sys.net>)

'''
