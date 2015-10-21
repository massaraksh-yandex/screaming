#!/bin/bash

kill -9 "$(ps ax | grep screaming.py -m1 | cut -f1 -d ' ')"
