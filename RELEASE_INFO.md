# Release Info

## Current Version: v0.3.0

**Release date:** 2026-09-30

## Overview

See [README](README.md) for full documentation and [CHANGELOG](CHANGELOG.md) for version history.

v0.3.0 is an infrastructure release: the site's own content is unchanged, but
the nginx vhost in `deploy.sh` now reproduces production exactly, and CI refuses
a deploy that has lost one of the blocks that were lost before.

## Installation

`ash
git clone https://github.com/Mukller/antonpetnitsky.com.git
cd antonpetnitsky.com
`

## Support

If you encounter any issues, please open an issue on GitHub.

---

**Author:** [Anton Petnitsky](https://github.com/Mukller)