from cx_Freeze import setup, Executable

setup(
    name="bot_tabela",
    version="1.0",
    description="Um bot maroto que utiliza uma tabela",
    executables=[Executable("bot_tabela.py")]
)
