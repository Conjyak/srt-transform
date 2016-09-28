# srt-transform

Shift and stretch a '.srt' subtitle file using a linear transform.

## Usage

```
usage: srt-transform.py [-h]
    --SW START_WRONG --SR START_RIGHT --EW END_WRONG --ER END_RIGHT INPUT OUTPUT

positional arguments:
  INPUT                 input srt file
  OUTPUT                output srt file

optional arguments:
  -h, --help            show this help message and exit
  --SW START_WRONG, --start-wrong START_WRONG
  --SR START_RIGHT, --start-right START_RIGHT
  --EW END_WRONG, --end-wrong END_WRONG
  --ER END_RIGHT, --end-right END_RIGHT

Copyright (c) 2016, Antonio Coratelli.
Released under BSD 3-Clause License. See 'LICENSE' file.
```

## Requirements

This indicator requires the following python modules: `os`, `sys`, `re`,
`argparse`.
You can install the missing ones using `pip` ([link][pip]).

## Support

If you like this application, you can [share it][support_share],
[buy me a coffe][support_paypal], or just say thanks adding a
[star][support_star] :)


[pip]: https://wiki.python.org/moin/CheeseShopTutorial#Installing_Distributions

[support_share]:  https://www.addtoany.com/share/#url=github.com/antoniocoratelli/srt-transform
[support_star]:   https://github.com/antoniocoratelli/srt-transform/stargazers
[support_paypal]: https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=YFBTBS8WWDTZS
