Set-Location 'c:\Users\hongq\Downloads\CSI-front-main\CSI-front-main'
git ls-remote https://github.com/hongq/wicare.git HEAD > tmp_lsremote.txt 2> tmp_lsremote_err.txt
[System.IO.File]::WriteAllText('tmp_lsremote_exit.txt', $LASTEXITCODE.ToString())
