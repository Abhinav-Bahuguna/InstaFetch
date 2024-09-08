import os
import requests

def downloader(URL, destination_directory, filename):
    with requests.get(URL, stream=True) as response:
        response.raise_for_status()

        if not os.path.exists(destination_directory):
            os.makedirs(destination_directory)

        with open(f'{destination_directory}/{filename}', 'wb') as f:
            for chunk in response.iter_content(chunk_size=4096):
                f.write(chunk)