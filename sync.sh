#!/bin/sh

chmod -R u=rwX,go=rX out
rsync \
    "$@" \
    --itemize-changes \
    --recursive \
    --perms \
    --delete \
    --exclude .websleydale_output_dir \
    --exclude /games \
    out/ \
    lemon.lumeh.org:/srv/http/lumeh.org/
echo >&2 "Reloading Caddy..."
ssh lemon.lumeh.org 'systemctl reload caddy'
