#!/bin/sh

chmod -R u=rwX,go=rX out
rsync \
    "$@" \
    --itemize-changes \
    --recursive \
    --perms \
    --delete \
    --exclude /games \
    out/ \
    lemon.lumeh.org:/srv/http/lumeh.org/
