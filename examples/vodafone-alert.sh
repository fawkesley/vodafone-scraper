#!/bin/bash -e

export VODAFONE_USERNAME="<SET TO YOUR USERNAME/EMAIL>"
export VODAFONE_PASSWORD="<SET TO YOUR PASSWORD>"

export DISPLAY=:99
Xvfb $DISPLAY -ac &
XVFB_PID=$!

vodafone-scraper alert --minutes=540 --megabytes=450

kill $XVFB_PID
