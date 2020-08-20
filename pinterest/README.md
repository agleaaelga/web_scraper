# Pinterest Board Scraper

Use selenium to download all images(.jpg/png) from a Pinterest board

## How does it work

Using selenium's automated testing environment, the scraper opens up the url for the Pinterest
board, login with your credentials, perform scrolling action and retrieve information from
`img srcset`, eventually saving them to local directories.  

### Prerequisites

Modules you need to install the software and how to install them

```
selenium
requests
```

### Installing
Install selenium using the following command:

```
pip install selenium
```

Install requests using the following command:

```
pip install requests
```

## Running the tests

automated testing for the program hasn't been written yet.

## Authors

* **Upperwatch** 

## Useful documentations for further read up

* https://www.selenium.dev/
* https://requests.readthedocs.io/en/master/

## Areas of improvement

* can't save gif files yet
* performance
