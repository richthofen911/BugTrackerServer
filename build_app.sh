#!/bin/bash

cd /home/admin/Programming/ap1/Proximity_dev/app/src/main/res/values/
# change bundleID
xmlstarlet ed -L -u "/resources/string[@name='idbundle']" -v $1 strings.xml
# change app_name
xmlstarlet ed -L -u "/resources/string[@name='app_name']" -v $2 strings.xml

# delete the old apk file
rm /home/admin/Programming/ap1/Proximity_dev/app/build/outputs/apk/app-debug.apk

#cd to the project's root directory
cd /home/admin/Programming/ap1/Proximity_dev
# build a new debug version apk
./gradlew assembleDebug
# cp the new built apk to my target directory
cp /home/admin/Programming/ap1/Proximity_dev/app/build/outputs/apk/app-debug.apk /home/admin/Proximity_derivative/$2.apk

