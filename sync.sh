#!/bin/sh

chmod -R u=rwX,go=rX out
rsync \
    "$@" \
    --itemize-changes \
    --recursive \
    --perms \
    --delete \
    --include /files/ \
    --include /files/public/ \
    --include /files/public/.header.html \
    --include /files/public/.footer.html \
    --exclude /files/public/* \
    --exclude /files/* \
    out/ \
    lemon.lumeh.org:/srv/http/lumeh.org/
