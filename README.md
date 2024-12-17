# Helldive.py


[![PyPI](https://img.shields.io/pypi/v/helldivepy.svg?label=PyPI&color=blue)](https://pypi.org/project/helldivepy/)
![PyPI - Downloads](https://img.shields.io/pypi/dm/helldivepy?color=brightgreen)
![GitHub License](https://img.shields.io/github/license/ajxd2/helldive.py?color=yellow)
[![Python Versions](https://img.shields.io/pypi/pyversions/helldivepy.svg?color=orange)](https://pypi.org/project/helldivepy/)
![GitHub contributors](https://img.shields.io/github/contributors/ajxd2/helldive.py?color=ff69b4)

> A simple Python library for diving deep into the [Helldivers Community API](https://github.com/helldivers-2/api) and [Diveharder API](https://github.com/helldivers-2/diveharder_api.py).

---

## 📕 Contents

- [Helldive.py](#helldivepy)
  - [📕 Contents](#-contents)
  - [⚙️ Installation](#️-installation)
  - [🚀 Quickstart](#-quickstart)
  - [🌟 Features](#-features)
  - [🔗 Links](#-links)

## ⚙️ Installation

To install **Helldive.py**, just use pip:

```bash
pip install helldivepy
```

## 🚀 Quickstart

Here's a super-quick example to get you diving right in:

```python
import helldivepy

client = helldivepy.ApiClient(user_agent="my-app", user_contact="email@example.com")

# Get the latest dispatches
dispatches = client.dispatch.get_dispatches()

print(dispatches)
# Output example
[
   Dispatch(id=0, published=datetime.datetime, type=0, message='Hello, World 1!'),
   Dispatch(id=1, published=datetime.datetime, type=0, message='Hello, World 2!'),
   Dispatch(id=2, published=datetime.datetime, type=0, message='Hello, World 3!')
 ]
```

## 🌟 Features

- **Easy API Access**: Communicate with the Helldivers Community API and Diveharder API without breaking a sweat.
- **Typed Data**: Get structured, easily readable data like dispatches, planets, and more!
- **Perfect for Projects**: Ideal for projects, bots, or just exploring Helldivers data.

---

## 🔗 Links

- [Contributing](./CONTRIBUTING.md)
- [Security](./SECURITY.md)
- [Code of conduct](./CODE_OF_CONDUCT.md)
- [DiveHarder](https://github.com/helldivers-2/diveharder_api.py)
- [Community API](https://github.com/helldivers-2/api)
- [API discussion Discord](https://discord.gg/MThYGMCqgp)
