# Add-on Downloader
Easily download Firefox add-ons from Mozilla's add-on website or from a custom URL.

## Why?
When configuring a new browser profile or a new computer, having easy access to the latest versions of your favorite add-ons drastically eases the installation process.

This is especially useful in environments where a standard set of add-ons is installed on all computers, but centralized add-on management is not in place.

## How?
1. Clone the repository
2. If necessary, install dependencies: `pip3 install -r requirements.txt`
3. Modify the addon-list.json file to include the IDs/URLs of the add-ons you want to download (see below).
4. Execute the script: `./addon-downloader.py`

All downloaded add-ons will be placed in the current directory.

### Finding an add-on's ID
You can use the search API to search for the add-on by name.

For example, modify this URL to use any search term:
```
https://services.addons.mozilla.org/en-US/firefox/api/1.5/search/adblock+plus
```

The first result is likely the one you are looking for:
```xml
<addon id="1865">
```

So, the Adblock Plus ID is `1865`.

You can now add this to the configuration:
```json
{
    "source": "amo",
    "name": "AdBlock Plus",
    "amoid": 1865
}
```

### Using an add-on's URL
If you have the direct URL for the XPI file (for example, [HTTPS Everywhere](https://www.eff.org/https-everywhere) lists the URL on their website), you can insert that URL directly into the configuration:
```json
{
    "url": "https://www.eff.org/files/https-everywhere-latest.xpi",
    "source": "url",
    "name": "HTTPS Everywhere"
}                
```

## Contributing
Looking to contribute? Submit an issue or pull-request.

Please be sure to check the LICENSE file.
