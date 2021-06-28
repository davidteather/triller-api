# triller-api
 The Unofficial Triller API Wrapper In Python

 [![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white&style=flat-square)](https://www.linkedin.com/in/davidteather/) [![Sponsor Me](https://img.shields.io/static/v1?label=Sponsor&message=%E2%9D%A4&logo=GitHub)](https://github.com/sponsors/davidteather)  [![GitHub release (latest by date)](https://img.shields.io/github/v/release/davidteather/triller-api)](https://github.com/davidteather/triller-api/releases) [![Build Status](https://travis-ci.com/davidteather/triller-api.svg?branch=master)](https://travis-ci.com/davidteather/triller-api) [![GitHub](https://img.shields.io/github/license/davidteather/triller-api)](https://github.com/davidteather/triller-api/blob/master/LICENSE) [![Downloads](https://pepy.tech/badge/trillerapi)](https://pypi.org/project/trillerapi/) ![](https://visitor-badge.laobi.icu/badge?page_id=davidteather.triller-api) [![Support Server](https://img.shields.io/discord/783108952111579166.svg?color=7289da&logo=discord&style=flat-square)](https://discord.gg/yyPhbfma6f)

## Getting Started

Run the following command to install it from PyPi
```sh
pip install TrillerAPI
```

Basic Quick Start Script
```py
import TrillerAPI
user = TrillerAPI.login("YOUR_TRILLER_USERNAME", "YOUR_TRILLER_PASSWORD")
trending = user.get_trending()
```

[Full Documentation](https://davidteather.github.io/triller-api/docs) (as of now you only have to read the TrillerAPI.user User class)
## TODO
- Discover posts
    - user's posts
    - trending music
    - trending hashtags
- Add documentation
- Quick start guide