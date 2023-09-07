#!/bin/bash

TOKEN=$1
if [ _${TOKEN} == _ ]; then
  echo "missing TOKEN, exiting..."
  exit 1
fi

echo "gcube_token,  ${TOKEN}" >globalvariables.csv
