#!/bin/bash

if [ -z ${BOT_ID+x} ];
  then export BOT_ID=$(python botsetup.py);
else
  echo 'BOT_ID already set';
fi
