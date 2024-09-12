@echo off
setlocal enabledelayedexpansion

for /r "E:\Git\Python_modules\dev\samuTest\examples\class_test\tests\classTestClient" %%a in (.) do (
    if exist "%%a" (
        pushd "%%a"
        for %%f in (*.json) do (
            set "foldername=%%~nxa"
            echo Renaming %%f to !foldername!.json
            ren "%%f" "!foldername!.json"
        )
        popd
    ) else (
        echo Folder not found: "%%a"
    )
)

endlocal
