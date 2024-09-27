#!/bin/bash
echo "Compiling JTML Todo App..."
python3 ../../../jtml_cli.py --input components/TodoApp.jtml --output index.html --progressive --pqtt
echo "Todo App Compiled!"
