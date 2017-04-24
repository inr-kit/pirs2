#!/bin/bash

# Generate graph of imports
sfood -v -r --internal ./pirs/__init__.py > pirs.sfood1
sfood-cluster -f pirs.clusters < pirs.sfood1 > pirs.sfood2
sfood-graph < pirs.sfood2 > pirs.dot
dot -v -Tpdf \
    -Gsize="11.692, 8.267!" \
    -Granksep="0.01" \
    -Gsep="1.0" \
    -Goverlap="true"  \
    -Gratio="compress" \
    -Gfontsize="8" \
    -Nshape="plaintext" \
    -Nfontsize="16" \
    -Earrowsize="0.5" \
    < pirs.dot > pirs.pdf
