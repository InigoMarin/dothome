#!/bin/bash

# this file contains all the environment variables
export PATH=$PATH:~/.local/bin

export EDITOR=nvim

# this is required to run kdenlive appimage
export $(dbus-launch)
