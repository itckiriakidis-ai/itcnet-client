# ITCNET

ITCNET is the remote support application of **I.T. Center KiriakidiS**
(Ταγματάρχη Χαϊλή 6, Αριδαία · +30 2384 50 18 50 · info@kiriakidis.biz · https://www.kiriakidis.biz).

It is based on [RustDesk](https://github.com/rustdesk/rustdesk) by Purslane Tech Pte. Ltd.,
and is distributed under the same license, the GNU Affero General Public License v3.0 (see `LICENCE`).
The complete source code of ITCNET is this repository.

## What is changed compared to RustDesk

- Name (ITCNET), icons, logos and accent color (`branding/apply_branding.py`)
- Default ID/relay server and key, taken at build time from the repository variables
  `ITCNET_SERVER` and `ITCNET_KEY` (Settings → Secrets and variables → Actions → Variables)

## Building

1. Settings → Actions: enable workflows for this repository.
2. Set the repository variables `ITCNET_SERVER` and `ITCNET_KEY`.
3. Actions → "Flutter Nightly Build" → Run workflow. The installers appear in the `nightly` release.

To regenerate icons and logos after changing `branding/icon-1024.png`:

```
pip install pillow
ITCNET_FONT=/path/to/Poppins-Bold.ttf python3 branding/apply_branding.py
```
