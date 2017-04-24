

Examples
==========

This section shows how the TSP package can be applied to tasks that often arise during preparation of 
complex input files. This covers inclusion of external files and templates and generation of a set of input 
files that differ by some parameter (for e.g. parametric studies).


Inclusion of external files
----------------------------
The TSP package provides no special mechanism to include external files into the resulting
file, however, one can use standard Python capabilities. In the following
example, an external file is read by the ``open`` [#]_ Python function and its
content is printed to the standard output. Since the standard output of the
snippet execution appears right after the snippet code, the file content will
appear in the resulting file.

.. [#] http://docs.python.org/library/functions.html#open

.. list-table::
    :header-rows: 1

    * - Template
      - Resulting file
    * - .. literalinclude:: examples/incl1.t

        where ``incl.txt`` has the following content: 
        
        .. literalinclude:: examples/incl.txt
     
      - .. literalinclude:: examples/incl1.t.res

The ``open`` function returns a file object that can be iterated line by line;
in the example above, the ``for`` loop iterates over all lines of the opened
file.  The file is opened with ``"r"`` key that means that the file is open
only for reading. Each line of the opened file is printed out. Note that the
print statement ends with the comma, this prevents extra empty lines in
the output. The snippet starts with the empty print statement, it adds a new
line just after the snippet's end marker in the resulting file, so that the
included file starts on the new line.


Inclusion of other templates
----------------------------
While in the above example inclusion of text file without any preprocessing is
shown, often it is necessary to include another template that needs first to be
preprocessed. To accomplish this task one needs to use directly the function
:func:`pre_pro` from the module :mod:`text_with_snippets` of the TSP package.
In simple situations this function is called by the preprocessor ``ppp.py`` so
that a user does not use it directly; this example shows how to use this
function directly in a template (or in a Python script).


The :func:`pre_pro` function  takes the name of a template file as argument and
returns the corresponding resulting file content as a multiline string.  This
function is imported by the script ``ppp.py`` and thus is accessible inside
snippets by default. To include the result of evaluation of another template,
simply call this function and print out its result:

.. list-table::
    :header-rows: 1

    * - Template 
      - Resulting file 
    * - .. literalinclude:: examples/incl2.t

        where ``itempl.txt`` has the following content: 
        
        .. literalinclude:: examples/itempl.txt

      - .. literalinclude:: examples/incl2.t.res

In this example, the snippet code is removed from the resulting file by
applying the ``-d`` snippet key. The snippet's output -- the result of
preprocessing of the template ``itempl.txt`` is thus written instead of the
snippet. To remove the extra new-line after the inserted template, the
``print`` statement is ended with comma.

      
Multiple resulting files for parametric studies
------------------------------------------------
Sometime it is necessary to prepare many input files differing from each other
by some parameters. This task can be automatized without writing many template
files or manually changing parameters in the template.

Since one can process a template file from another template, one can call the
main template from within a wrapper, where certain value of parameter is set.
Let say we want to prepare three input files described by the following template,
so that the input files differ only by the value of parameter ``N``::

    ''
    c Input file for 'N = 1'.
    c Some lines depending on
    c the value of 'N'.

Three different input files can be created by sequentially changing the value
of ``N`` in the template, processing the template and saving the resulting file
under a unique name. Alternatively, one can process this template from another
one, and write the result of processing not to standard output, but to a file.
Let the above template is saved in the file ``main.t``. The wrapper template could look
like:


.. list-table::
    :header-rows: 1

    * - Template 
      - Generated files
    
    * - .. literalinclude:: examples/wrapper.t
        
      - The first generated file, ``input_V1``:

        .. literalinclude:: examples/input_V1

        the last generated file, ``input_V3``:

        .. literalinclude:: examples/input_V3

where ``main.t``  is

.. literalinclude:: examples/main.t

Note that the main template was slightly modified: the snippet defining the
value of ``N`` is disabled by the ``-s`` key. It is not needed here anymore,
since ``N`` is defined in the wrapper template. Processing the wrapper template
with ``ppp.py`` will result in three files named ``input_V1``, ``input_V2`` and 
``input_V3`` that will differ from each other only by the value of variable ``N``.



