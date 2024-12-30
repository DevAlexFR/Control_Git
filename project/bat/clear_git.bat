@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

rem Define o caminho raiz para o diretório onde o .bat está localizado
set "root_path=%~dp0"

echo Iniciando a busca e remoção de diretórios .git em %root_path%
echo.

rem Função para deletar diretórios ocultos .git em pastas diretamente no diretório raiz
:delete_git_dirs
for /d "%root_path%\*" %%d in (*) do (
    echo Inspecionando %%d
    if exist "%%d\.git" (
        echo Deletando %%d\.git
        attrib -h -s "%%d\.git"
        rd /s /q "%%d\.git"
        echo Deletado da pasta %%d\.git
        echo.
    )
)

:end
echo Terminado.
pause
