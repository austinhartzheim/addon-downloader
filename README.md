# Add-on Downloader
Easily download Firefox add-ons from Mozilla's add-on website or from a custom URL.

## Why?
When configuring a new browser profile or a new computer, having easy access to the latest versions of your favorite add-ons drastically eases the installation process.

This is especially useful in environments where a standard set of add-ons is installed on all computers, but centralized add-on management is not in place.

## How?
1. Clone the repository
2. Modify the script to include the IDs of the add-ons you want to download (see below).
3. Execute the script/

### How to find an add-on's ID
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
```python
{
    'name': 'AdBlock Plus',
    'source': 'amo',
    'amoid': 1865
}
```

### Adding an add-on by URL
If you have the direct URL for the XPI file (for example, [HTTPS Everywhere](https://www.eff.org/https-everywhere) lists the URL on their website), you can insert that URL directly into the configuration:
```python
{
    'name': 'HTTPS Everywhere',
    'source': 'url',
    'url': 'https://www.eff.org/files/https-everywhere-latest.xpi'
}
```

## Contributing
Looking to contribute? Submit an issue or pull-request.

Please be sure to check the LICENSE file.
