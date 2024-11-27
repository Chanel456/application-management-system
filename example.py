import validators

def validate_url(url):
    """ Validate the given URL using the validators library. :param url: URL to be validated. :return: True if the URL is valid, otherwise False. """
    if validators.url(url):
        return True
    else: return False
        # Example usage

urls_to_check = [
    "https://www.example.com",
    "ftp://ftp.example.com",
    "http://localhost",
    "https://happy.com" ]

for url in urls_to_check:
    if validate_url(url):
        print(f"URL is valid: {url}")
    else:
        print(f"URL is not valid: {url}")