#!/bin/bash


# si es que hay cambios bajarlos
git pull origin main

# subir cambios a git
git add .
git commit -m "cambios"
git push origin main
