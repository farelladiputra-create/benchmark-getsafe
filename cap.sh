#!/bin/bash
# cap.sh <outfile> <expected-resource-id>
# Screenshots the current emulator state and confirms which screen it is
# by looking for a marker resource-id in the uiautomator dump.
A=/opt/homebrew/bin/adb
OUT="$1"; MARK="$2"
$A shell uiautomator dump /sdcard/wd.xml >/dev/null 2>&1
sleep 1
$A pull /sdcard/wd.xml /tmp/wd.xml >/dev/null 2>&1
if [ -n "$MARK" ] && grep -q "$MARK" /tmp/wd.xml; then
  echo "OK   $OUT  ($MARK found)"
else
  echo "WARN $OUT  (marker '$MARK' NOT found)"
fi
$A exec-out screencap -p > "$OUT"
