#!/bin/bash

if [ -z "$MEGA_EMAIL" ]; then
	echo "$(date): MEGA_EMAIL not set, skipping login"
	exit 0
else
	echo "$(date): Logging in to MEGA..."
	if [ -z "$MEGA_PASSWORD" ]; then
		echo "$(date): Error: No password provided"
		exit 1
	else
		mega-login "$MEGA_EMAIL" "$MEGA_PASSWORD" || exit 1
	fi
fi
