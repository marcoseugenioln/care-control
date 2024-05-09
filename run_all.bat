start "webapp" run_app test_config.json /B

echo "Runnning all tests"

python -m unittest discover -s server.test -p "*_test.py"

set "PID="
for /f "tokens=2" %%A in ('tasklist /FI "WINDOWTITLE eq webapp*" /FI "Status eq Running" 2^>NUL') do @Set "PID=%%A"
if defined PID taskkill /F /PID %PID%
for /f "tokens=2" %%A in ('tasklist /FI "WINDOWTITLE eq webapp*" /FI "Status eq Running" 2^>NUL') do @Set "PID=%%A"
if defined PID taskkill /F /PID %PID%
