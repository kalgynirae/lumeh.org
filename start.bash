#!/usr/bin/env bash

pane=$(tmux split-window -h -f -l 30% -P -F '#{pane_id}') || exit 1
tmux send-keys -t "$pane" -l $'watchexec -i urls.txt ./build.sh\n'

pane=$(tmux split-window -t "$pane" -v -l 25% -P -F '#{pane_id}') || exit 1
tmux send-keys -t "$pane" -l $'./test.sh\n'

tmux select-pane -t "$TMUX_PANE"
xdg-open http://localhost:4000/
