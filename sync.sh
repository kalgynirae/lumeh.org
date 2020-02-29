#!/bin/sh

chmod -R u=rwX,go=rX out
rsync \
    "$@" \
    --checksum \
    --itemize-changes \
    --recursive \
    --perms \
    --times \
    --delete \
    --exclude files/ \
    out/ \
    lemon.lumeh.org:/srv/http/lumeh.org/
