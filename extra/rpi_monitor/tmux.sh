SESSION=rpi_monitor
if tmux attach-session -t $SESSION; then
    echo "session exists; attaching"
else
    echo "create new session"
    tmux new -s $SESSION -d
    tmux source ~/.config/tmux/tmux.conf
    tmux split-pane -t $SESSION:0.0
    tmux split-pane -t $SESSION:0.0
    tmux select-layout even-vertical
    tmux select-layout -t $SESSION even-vertical
    tmux send-keys -t rpi_monitor:0.0 
    tmux send-keys -t $SESSION:0.0 "~/.config/tmux/plugins/tmux-logging/scripts/toggle_logging.sh" Enter
    tmux send-keys -t $SESSION:0.1 "~/.config/tmux/plugins/tmux-logging/scripts/toggle_logging.sh" Enter
    tmux send-keys -t $SESSION:0.2 "~/.config/tmux/plugins/tmux-logging/scripts/toggle_logging.sh" Enter
    tmux send-keys -t $SESSION:0.0 "cd ~/rpi_monitor/" Enter
    tmux send-keys -t $SESSION:0.1 "tio /dev/ttyAMA0" Enter
    tmux send-keys -t $SESSION:0.2 "tio /dev/ttyACM0" Enter
    tmux select-pane -t $SESSION:0.0
    tmux attach-session -t "$SESSION"
fi


