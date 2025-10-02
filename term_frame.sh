#!/usr/bin/env bash

# Term Frame: draw a status bar at the top of the terminal indicating SSH state.

_term_frame_draw_bar() {
    [[ $- != *i* ]] && return
    command -v tput >/dev/null 2>&1 || return

    local cols
    cols=$(tput cols 2>/dev/null)
    [[ -z $cols || $cols -le 0 ]] && cols=80

    local label color_bg
    if [[ -n ${SSH_CONNECTION:-} ]]; then
        color_bg=$'\e[41m'
        label="${USER}@$(hostname)"
    else
        color_bg=$'\e[42m'
        label="${USER}@$(hostname)"
    fi

    label="     ${label}"

    if (( ${#label} > cols )); then
        label=${label:0:cols}
    fi

    local fill=$((cols - ${#label}))

    tput sc
    tput cup 0 0
    printf '%s%s' "$color_bg" "$label"
    if (( fill > 0 )); then
        printf '%*s' "$fill" ''
    fi
    printf '\e[0m'
    tput rc
}

_term_frame_setup() {
    [[ $- != *i* ]] && return
    case ${TERM:-} in
        xterm*|screen*|tmux*|rxvt*|vt100|linux) ;;
        *) return ;;
    esac

    if [[ -z ${TERM_FRAME_PROMPT_COMMAND_SET:-} ]]; then
        TERM_FRAME_PROMPT_COMMAND_SET=1
        if declare -p PROMPT_COMMAND 2>/dev/null | grep -q '^declare -a'; then
            PROMPT_COMMAND=(_term_frame_draw_bar "${PROMPT_COMMAND[@]}")
        elif [[ -n ${PROMPT_COMMAND:-} ]]; then
            PROMPT_COMMAND="_term_frame_draw_bar;${PROMPT_COMMAND}"
        else
            PROMPT_COMMAND="_term_frame_draw_bar"
        fi
    fi
}

_term_frame_setup

# vim: ft=sh
