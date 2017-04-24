.. |ppp| replace:: ``ppp.py``

How to use TSP
#################

Basic usage of the TSP package is to simplify preparation of input decks
for computer codes with limited syntax possibilities. Instead of writing an
input deck directly, a template can be written that generally has syntax
and structure of the input deck, but also can include Python code snippets,
which will be replaced in the resulting file. Thus one can e.g. define and
use variables, include external files, even if these operations are not
permitted by the input file syntax of the target computer code. Ultimately,
one gets possibility to use the whole legacy of Python when writing an input
deck.

The TSP preprocessor, an executable script called ``ppp.py``, is used to
process templates. If a template file is stored in file ``input.t``, the following
command::

    $ ppp.py input.t

will generate the file called ``input.t.res`` that contains the result of
processing.

The content of the template file is logically divided into two parts. The
template's first line is used to set the delimiters for the 
snippets and to specify some other options. The rest of the template file, i.e.
everything from its second line till the end of file, defines the content
of the resulting file (it is called below **template body**). It is
arbitrary text, interlaced with Python snippets, the latter must be marked
with delimiters defined at the first line. Details see in Section
:ref:`template-syntax`.

There are two types of snippets, **evaluation snippets** and
**executable snippets**. Evaluation snippets are substituted by the
result of evaluation.  Executable snippets are copied into the resulting
file, but if any standard output is generated during their execution, it is
appended to the snippet in the resulting file. For details see
:ref:`snippets-processing`.

There are options that control the appearance of sippets in the
resulting file, see :ref:`keys-label`. The multi-line snippets can be
commented out in the resulting file, see :ref:`multi-line-snippets`. 


Installation
============

To install the TPS package, unzip ( untar) the downloaded archive, go
to the created directory containing file ``setup.py`` and run 

.. code-block:: bash

    $ python setup.py install

This command will install files into the default location, which for a Linux-based OS
is in ``/usr/local`` and requires administrator priviledges.  Alternatively,
one can install the package locally, using the command line option ``--user``:

.. code-block:: bash

    $ python setup.py install --user

For details see [#]_. 

.. [#] http://docs.python.org/install/index.html.   

The TSP package provides the script called ``ppp.py``. During the installation
process, the script will be copied into the directory where the Python
interpreter is installed (under Windows it can be something like
``c:\Python27\Scripts``) and thus will be available at the command prompt. The
installation is sucsessful, if the script is available at the command line, and
when called without a command line parameter, generates the following message:    

.. literalinclude:: examples/message.txt    

Script |ppp| uses function :func:`pre_pro`, defined in the module
:mod:`text_with_snippets` of the TSP package. Although the most common use of
TSP is to call |ppp| script from the terminal command line, one can also import
this function and use it from the Python interpreter or in a Pyhon script.

The name of the text file to be processed must be given to |ppp| as a command
line argument. The output file will have the name of the input file, with
suffix ``.res``. So far the TSP package is installed, the |ppp| script should
be availabe at the command line, and the command

.. code-block:: bash

    $ ppp.py input

should result in a new file called ``input.res``.    
    


.. _template-syntax:

Structure of template file
==========================
Generally, the content of a template file consists of the first line with
information for the preprocessor, followed by arbitrary text interlaced with
Python snippets. 

Python snippets must be marked at the beginnig and at the end by the characters
specified at the first line.  Optionally, each snippet can be prefixed with a
key that specifies details of how the snippet code and its
evaluation/execution result appears in the resulting file. For available keys see :ref:`keys-label`.

Inside snippets, the snippet delimiting characters cannot be used, in all other
respects a snippet must represent valid Python code.


.. _first-line:

The first line
---------------

The template's first line must contain information about snippet delimiters.
Optionally, it can also contain the commenting string, which will be used to comment
out the multi-line snippets in the resulting file, and the default key, which will
be applied to all snippets.

The snippet delimiting characters are the last two characters of the first line
with trailing spaces stripped off. They must be specified, i.e. the first line
must have at least two characters. An example of an minimalistic first line is shown on the
following template ::

    ''
    Simple text and snippets: 'i=1', 'i'.

In this template, the apostrophe, ``'``, is used to mark both the beginning and
the end of the snippets. Any characters can be used as delimiters, although in the case of
alphanumeric delimiters, a warning message will be issued. In the following template, character ``y`` is
used to mark the snippet's begin, and characher ``z`` -- to mark the snippet's end:

.. list-table::
    :header-rows: 1

    * - Template
      - Resulting file
    * - .. literalinclude:: examples/alphanum.t
      - .. literalinclude:: examples/alphanum.t.res

This template is processed with the following warning message:

.. literalinclude:: examples/log.alphanum.t


After the delimiters are read from the first line, it is
searched for a substring representing a valid key (possible keys see in
:ref:`keys-label`). If such substring is found, it will be used as the default
snippet key. The following example shows the first line specifying ``-l`` key as the default one::

    -l''
    All snippets in this template will have the -l option, 
    if no other key is specified.

Only the first substring matching one of the available keys will be taken into account.    

Additionally, in the  first line one can define a string of commenting
characters. It is used to comment out multi-line snippets in the resulting
file. The commenting string is the rest of the first line after stripping the
trailing spaces, reading (and removing) the delimiting characters and reading
(and removing) the default key.  The commenting string can be empty, as in the
examples above, in this case the multi-line snippets will appear in the
resulting file as is, without commenting out. In this case a warning is issued. 

Example 1
~~~~~~~~~~

In the following example, the commenting string consists of character ``c``
followed by one space, the delimiters are quotes ``'``:

.. list-table::
    :header-rows: 1

    * - Template
      - Resulting file
    * - .. literalinclude:: examples/firstline1.t
      - .. literalinclude:: examples/firstline1.t.res

This template describes a part of an MCNP input file, where ``C`` or
``c`` character at the first five positions of a line followed by a space means that
this line is a comment.

Example 2
~~~~~~~~~~

This example differs from the previous one by the first line only, where the default snippet
key is set to ``-l``: 

.. list-table::
    :header-rows: 1

    * - Template
      - Resulting file
    * - .. literalinclude:: examples/firstline2.t
      - .. literalinclude:: examples/firstline2.t.res

The commenting string is ``'c '``, the default key is ``-l`` and both
delimiters are ``'``.  This example is similar to the previous one, except the
default positioning of the snippet evaluation results is changed. By default,
the space allocated by a snippet is not preserved (the ``-D`` option), here we
specified another default behaviour: if the snippet evaluation result is
shorter than the snippet itself, the result will be adjusted left (the ``-l``
option). With this option, the resulting file can be more similar to the
template file, as compared with the resulting file obtained with default ``-D``
option.

Note that the key specified in the first line defines the default key; each snippet still can be 
preceded with its own key that overwrites the default one.

Example 3
~~~~~~~~~~

The commenting string is ``# -r``, the default key is ``-l``, the beginning
delimter is the back quote, `````, and the end delimiter is the single quote,
``'``:

.. list-table:: 
    :header-rows: 1

    * - Template
      - Resulting file
    * - .. literalinclude:: examples/firstline3.t
      - .. literalinclude:: examples/firstline3.t.res

This example illustrates that the default key and the commenting string can be 
specified in arbitrary order. Note that only the first substring that matches the key pattern is
taken into account. The rest of the line (after removing the delimiters and the default key)
is considered as the commenting string.


.. _snippets:   

Template's body
------------------
Everything after the template's first line constitutes the template's body
that contains arbitrary text and Python snippets.

Inside the template body, snippets must be delimited at the beginning and at
the end by characters specified in the first line. The beginning delimiter can
be preceded with any other character, and the end delimiter can be followed by
any other character. In the following example, text within quotes will be
recognized by the preprocessor as a snippet:
    
.. list-table::
    :header-rows: 1

    * - Template
      - Resulting file
    * - .. literalinclude:: examples/snippet1.t
      - .. literalinclude:: examples/snippet1.t.res

A snippet prefix consisting of the minus sign followed by a letter can have
special meaning. If it coincides with one of the snippet keys (see in
:ref:`keys-label`) , the snippet representation in the resulting file will be
changed and the prefix will not appear in the resulting file. Examples of
snippet prefixes:
    
.. list-table::
    :header-rows: 1

    * - Template 
      - Resulting file 
    * - .. literalinclude:: examples/keys2.t
      - .. literalinclude:: examples/keys2.t.res

The snippet delimiter characters cannot be used inside snippets, since they
would be considered by the preprocessor as the beginning or end of the snippet.
Usually, this limitation can be simply overcome by choosing proper delimiting
characters. [#]_

.. [#] Note that in Python one can use interchangeably single and double quotes for strings.

All snippets are evaluated or executed in the common namespace. This means that 
a variable defined in one snippet will be "seen" in the following snippets.
Similarly, modules loaded in a snippet will become available in all consequent
snippets. This is also valid for inclusion of external templates: when a snippet
calls the :func:`pre_pro` function to process another template, all
variables defined in the processed template will become available in the
"calling" template. 
    




.. _snippets-processing:

Processing of snippets
======================

A snippet can be evaluated or executed. When a snippet is found, the
preprocessor first tries to evaluate it using the ``eval`` [#]_ Python built-in
function, and if the evaluation causes the ``SyntaxError``, the snippet will
be executed using the ``exec`` [#]_ Python built-in function. Thus, if a snippet code
is an expression [#]_ (for example, ``b``, ``a + b`` are expressions) it will be
evaluated, and if a snippet is a statement [#]_ (or several statements taking
several lines), it will be executed.


.. [#] http://docs.python.org/library/functions.html#eval 
.. [#] http://docs.python.org/reference/simple_stmts.html#exec
.. [#] http://docs.python.org/reference/expressions.html
.. [#] http://docs.python.org/reference/simple_stmts.html

When a snippet is evaluated, the string representation of the evaluation result
will substitute the snippet code in the resulting file. When a snippet is
executed, its code is repeated in the resulting file and standard output
generated by the snippet will be caught and put right after the snippet code.
This default behaviour can be modified to some extent by the snippet keys,
described in the section :ref:`keys-label`.

Evaluation examples
-------------------
When a snippet is evaluated and the evaluation result substitutes the snippet
code in the resulting file, several situations are possible.  If the resulting
string is longer or shorter than the snippet code, the text on the line
after the snippet will be shifted in the resulting file:

.. list-table::
    :header-rows: 1

    * - Template 
      - Resulting file 
    * - .. literalinclude:: examples/eva1.t
      - .. literalinclude:: examples/eva1.t.res

    
Note, in the template's 3-rd line, the snippet code ``'c'`` takes 3 characters
(the delimiters are counted as well) and it is substituted with a string of 6 characters
``abcdef`` in the result. In the 9-th line the snippet ``'LongVariable'``
that takes 14 characters in the template, is replaced with only one character ``'a'``.

If the evaluation result is shorter than the snippet code, the default behaviour
can be changed using :ref:`keys-label`.
If the resulting string and the snippet code have the same length, the text
after the snippet will remain its position.


Execution examples
------------------
In the following example, the first snippet, ``'a="abc"'`` is executed. The
second snippet that is just the variable reference, ``'a'`` is evaluated, and
the third snippet that contains the ``print`` statement, is again executed:

.. list-table::
    :header-rows: 1

    * - Template 
      - Resulting file
    * - .. literalinclude:: examples/exe1.t
      - .. literalinclude:: examples/exe1.t.res

Note that by default, the print [#]_ Python statement adds the new-line character
at the end of the printed line, therefore in the above example the rest of the
line after the last snippet jumped onto the next line. To avoid the new-line
character, the comma-ended variant of the print statement should be used, e.g.
``'print a,'``.

.. [#] http://docs.python.org/reference/simple_stmts.html#print


.. _multi-line-snippets:

Multi-line snippets
-------------------

A snippet can take several lines, in this case it is always executed. The usual
indentation rules for Python code should apply to the multi-line snippets.
Consider the following template:


.. list-table::
    :header-rows: 1

    * - Template
      - Resulting file 
    * - .. literalinclude:: examples/mline1.t
      - .. literalinclude:: examples/mline1.t.res


The multi-line snippet here has 4 lines. The first line of the snippet is
empty: it starts right after the opening apostrophe and goes till the end of
the line. The 2-nd, 3-rd and 4-th lines contain Python statements that are 
indented, i.e. start at 5-th position. The indentation of the first
statement is optional and used in this example to visually distinguish the
snippet from the surrounding text. This indentation will be removed by the
preprocessor before passing the snippet to execution. Indentation of the
following statements should follow the Python rules. 

The code can start on the first snippet line as well, but in this case one
should take care about the proper indentation. The following example would
cause the indentation error, since the first code line has no indentation and
the other lines are indented (the snippet execution will be aborted so that no
standard output will be generated): 

.. list-table::
    :header-rows: 1

    * - Template 
      - Resulting file 
    * - .. literalinclude:: examples/mline2.t
      - .. literalinclude:: examples/mline2.t.res

This template would produce the following output:

.. literalinclude:: examples/log.mline2.t

The right way to put the code into the first snippet line is:

.. list-table::
    :header-rows: 1

    * - Template 
      - Resulting file 
    * - .. literalinclude:: examples/mline3.t
      - .. literalinclude:: examples/mline3.t.res

Note that this form is visualy less clear than in the first example in this
section, so it is better to avoid putting any code to the first line of the
multi-line snippet.

Multi-line snippets are always executed. By default, the code of the multi-line
snippets is repeated in the resulting file (for the other behaviour use ``-d`` key,
see :ref:`keys-label`), and if any standard output is generated by the snippet,
it is placed right after the snippet's end delimiter, on the same line.

When a multi-line snippet is repeated in the resulting file, all lines of the
snippet code, except the first one, are commented out by appending the string of
commenting characters to every snippet line. The commenting string is
defined in the template first line, see :ref:`first-line`. In the following template, the
two-characters string ``'c '`` (character ``c`` followed by the space) will be
used to comment mulitline snippets:

.. list-table::
    :header-rows: 1

    * - Template 
      - Resulting file 
    * - .. literalinclude:: examples/mline4.t
      - .. literalinclude:: examples/mline4.t.res

The string of commenting  characters defined in the templates's first line can
be empty. In this case a warning message will be printed and multi-line
snippets will not be commented out in the resulting file.

The standard output of the multi-line snippet is added right after the snippet
code, on the same line. In this case the first line of the output can become
commented out, like in the following example:

.. list-table::
    :header-rows: 1

    * - Template 
      - Resulting file 
    * - .. literalinclude:: examples/mline5.t
      - .. literalinclude:: examples/mline5.t.res

Sometimes, it is desired to put the snippet output on extra lines. To do this, 
use additional ``print`` statements in the snippet code. The above example would be:

.. list-table::
    :header-rows: 1

    * - Template 
      - Resulting file 
    * - .. literalinclude:: examples/mline6.t
      - .. literalinclude:: examples/mline6.t.res


.. _keys-label:

Optional snippet keys
---------------------
Optionally, a snippet can be prefixed with a key. A key consists of the
minus sign followed by a character, and must precede the snippet starting
delimiter without any blanks. The default key can be specified at the template first
line. It will apply to all snippets without keys.

Currently, the following keys are defined:

     ============= =================================
        Key        Meaning                          
     ============= =================================
        ``-D``     default. Do not preserve place
        ``-r``     adjust evaluation result right   
        ``-l``     adjust evaluation result left    
        ``-c``     center evaluation result         
        ``-d``     delete snippet code              
        ``-s``     skip snippet evaluation          
     ============= =================================

Keys ``-D``, ``-r``, ``-l``, and ``-c`` specify how the result of snippet
evaluation should be aligned within the place allocated by the snippet code (if
no key is given before the snippet and no default key is specified at the first
template line, the ``-D`` key will apply, i.e.  the snippet's place will not be preserved).
These keys have meaning only if a snippet is evaluated, i.e. when the evaluation
result should fit into the place allocated by the snippets code.

Key ``-d`` will delete the snippet code, so that the code will not enter the
resulting file.  In the case of snippet evaluation, the snippet will be
evaluated, but nothing will go to the resulting file. If the snippet is
executed, the resulting file will contain only the standard output of the
execution, not the snippet code itself.

Key ``-s`` specifies that the snippet should not be evaluated nor executed. In
this case, the snippet code is simply copied into the resulting file.

Snippet keys, except ``-s``, do not appear in the resulting file.

The meaning of the keys should be clear form the following example:

.. list-table::
    :header-rows: 1

    * - Template 
      - Resulting file 
    * - .. literalinclude:: examples/keys1.t
      - .. literalinclude:: examples/keys1.t.res


