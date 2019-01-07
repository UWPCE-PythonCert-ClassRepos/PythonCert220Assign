#!/bin/bash
# document

if [ "$#" -ne  "3" ] ; then
    echo "Useage: qc <package> <module> <file>"
    exit
fi

pytest --cov=$1 --pylint --pylint-rcfile=pylint.rc --pylint-error-types=EW $1/$2/$3 tests/$3
