<a href="https://www.hardwario.com/"><img src="https://www.hardwario.com/ci/assets/hw-logo.svg" width="200" alt="HARDWARIO Logo" align="right"></a>

# Host Application - HARDWARIO Control Tool

[![Travis](https://img.shields.io/travis/hardwario/bch-control-tool/master.svg)](https://travis-ci.org/hardwario/bch-control-tool)
[![Release](https://img.shields.io/github/release/hardwario/bch-control-tool.svg)](https://github.com/hardwario/bch-control-tool/releases)
[![License](https://img.shields.io/github/license/hardwario/bch-control-tool.svg)](https://github.com/hardwario/bch-control-tool/blob/master/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/bch.svg)](https://pypi.org/project/bch/)
[![Twitter](https://img.shields.io/twitter/follow/hardwario_en.svg?style=social&label=Follow)](https://twitter.com/hardwario_en)

This repository contains HARDWARIO Control Tool.

## Installing

You can install **bch** directly from PyPI:

```sh
sudo pip3 install -U bch
```

## Usage

```
bch --help
Usage: bch [OPTIONS] COMMAND [ARGS]...

Options:
  --gateway TEXT                 Gateway name [default: usb-dongle].
  -H, --mqtt-host TEXT           MQTT host to connect to [default: 127.0.0.1].
  -P, --mqtt-port INTEGER RANGE  MQTT port to connect to [default: 1883].
  --mqtt-username TEXT           MQTT username.
  --mqtt-password TEXT           MQTT password.
  --mqtt-cafile PATH             MQTT cafile.
  --mqtt-certfile PATH           MQTT certfile.
  --mqtt-keyfile PATH            MQTT keyfile.
  --base-topic-prefix TEXT       MQTT topic prefix [default: ''].
  -v, --verbosity LVL            Either CRITICAL, ERROR, WARNING, INFO or
                                 DEBUG

  --version                      Show the version and exit.
  -h, --help                     Show this message and exit.

Commands:
  gw       Gateway
  node
  pairing
  pub
  sub      Subscribe topic.

```

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT/) - see the [LICENSE](LICENSE) file for details.

---

Made with &#x2764;&nbsp; by [**HARDWARIO a.s.**](https://www.hardwario.com/) in the heart of Europe.
