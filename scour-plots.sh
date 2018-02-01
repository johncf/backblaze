#!/bin/bash
TMPDIR=/tmp
echo 'set -e'
cat plot-metadata | \
    awk -F'|' '{print "scour -i", $1, "-o '$TMPDIR'/scour.tmp.svg --shorten-ids && \
                       scour -i '$TMPDIR'/scour.tmp.svg -o", $1, "--enable-viewboxing \
                             --enable-id-stripping --enable-comment-stripping --indent=none"}'
# running scour twice like this is about 20% better than running it once with all flags!
echo 'rm -f '$TMPDIR'/scour.tmp.svg'
