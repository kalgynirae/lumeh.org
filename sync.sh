#!/bin/sh

chmod -R u=rwX,go=rX out
rsync \
    --itemize-changes \
    --recursive \
    --perms \
    --delete \
    --exclude blog/ \
    --exclude events/ \
    --exclude files/ \
    --exclude forum/ \
    --exclude guess/ \
    --exclude lymjeh/ \
    --exclude music/ \
    --exclude wiki-old/ \
    --exclude 400.shtml \
    --exclude 401.shtml \
    --exclude 403.shtml \
    --exclude 500.php \
    --exclude 500.shtml \
    --exclude colin-schedule.pdf \
    --exclude japanese_names.py \
    out/ \
    chanspac@host207.hostmonster.com:\~/public_html/lumeh/
