.. role:: raw-latex(raw)
    :format: latex

Conclusion and acknowledgement
==================================

Basic usage of the TSP package is to simplify preparation of input decks
for computer codes with limited syntax possibilities. Instead of writing an
input deck directly, a template can be written, which generally has syntax
and structure of the input deck, but also can include Python code snippets,
which will be replaced in the resulting file. Thus one can e.g. define and
use variables, include external files, even if these operations are not
permitted by the input file syntax of the target computer code. Ultimately,
one gets possibility to use the whole legacy of Python when writing input
decks.

TSP was used by the author to generate input files for MCNP code
:raw-latex:`\cite{mcnpREF}` and KANEXT system :raw-latex:`\cite{kanext}` under
Linux and Windows operating systems.

Current version of the package provides the following features:
    
    * Snippet keys to define positioning of the result and to skip the snippet's evaluation.
    * Multi-line snippets are optionally commented out in the resulting file.
    * Snippet delimiters and the string of commenting characters can be set arbitrarily.
    * Warning messages if alpha-numeric characters are used as snippets delimiters. This should warn a user 
      in the case he (she) forgets to specify the template's first line.
    * Warning messages that specify line number of a snippet that cannot be executed.

The package is currently not actively developed, since it already provides
features necessary to prepare input decks effectively. However, future
improvements can include the following:

    * more flexible format to define snippets output 
      formatting, like default formatting for integers, floats, etc.  
    * Specification of the default snippet key, commenting characters and delimiters
      in the preprocessor command line rather than in the template's first line.

The TSP Python package has been written during work on several projects funded
by the European Commission: ELSY :raw-latex:`\cite{ELSY}`, LEADER
:raw-latex:`\cite{LEADERWEB}` and CDT :raw-latex:`\cite{CDT09}`.


