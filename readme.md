# sarooar

some tools for saroo i found useful for myself, needs some clarification on some things

use at your own risk

report firmware version based on hash
```
python3 main.py -id --fw-path /mnt/SAROO/
Filename: saroocfg.txt is saroocfg.txt from SAROO firmware version: 0.6
Filename: ssfirm.bin is ssfirm.bin from SAROO firmware version: 0.6
Filename: mcuapp.bin is mcuapp.bin from SAROO firmware version: 0.6

```

check validity of fix library
```
$ python3 main.py -ck
Incorrect Length: GS-9189 V1.017 14 (for firmware v0.05 or less)
Incorrect Length: T-16207H V1.000 15 (for firmware v0.05 or less)
Incorrect Length: MK-81076 V1.001 15 (for firmware v0.05 or less)
Incorrect Length: T-4507G V1.002 14 (for firmware v0.05 or less)
Incorrect Length: MK-81307 V1.000 15 (for firmware v0.05 or less)
Incorrect Length: T-36001G V1.001 15 (for firmware v0.05 or less)
```

diff data collection against library
```
$ python3 main.py -df --ini-path datasets/chinaemu.org-read-htm-tid-129470.ini 
 [T-159056V1.000] needs GAME_ID length correction
```

most of the fixes came from the williamdsw repo with invalid data tweaked

i suppose if for some reason you want your fixes removed raise an issue

sai
