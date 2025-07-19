#!/bin/bash

if [[ ! -d ./build ]]; then
  mkdir ./build
fi

version=$1
if [[ -z $version ]]; then
  echo "build [version]"
  exit 0
fi

cd src
zip -r ../build/bob-plugin-cambridge-dict_v$version.bobplugin . *
cd ..

open build/bob-plugin-cambridge-dict_v$version.bobplugin