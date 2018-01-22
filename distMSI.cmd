python freezeSetup.py bdist_msi

RD build /s /q
MOVE dist "C:/Users/MarioRaul/Desktop/MyProject Builds/build - 2017.05.19/msi-exe.win32-3.6"
echo Compilation complete
PAUSE