@echo off
set  test_file=%1

start "webapp" run_app config-test.json /B

python -m unittest discover -s server.test -p %test_file%

set "PID="
for /f "tokens=2" %%A in ('tasklist /FI "WINDOWTITLE eq webapp*" /FI "Status eq Running" 2^>NUL') do @Set "PID=%%A"
if defined PID taskkill /F /PID %PID%
for /f "tokens=2" %%A in ('tasklist /FI "WINDOWTITLE eq webapp*" /FI "Status eq Running" 2^>NUL') do @Set "PID=%%A"
if defined PID taskkill /F /PID %PID%

timeout 1
del test.db