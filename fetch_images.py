import base64
import hashlib
import io
from pathlib import Path
import argparse
from multiprocessing import Pool
from tqdm import tqdm
from PIL import Image, ImageOps
import traceback
from urllib.request import Request, urlopen
import http.client
http.client._MAXHEADERS = 1000


def tqdmupdate(result):
    try:
        pbar.set_description(result[-10:])
        pbar.update()
    except:
        pbar.update()


def resize_save_image(data, dst_path, shape=(512, 512)):
    try:
        image = Image.open(io.BytesIO(data)).convert('RGB')
        image.thumbnail(shape)
        # image = ImageOps.fit(image, shape)
        image.save(dst_path)
    except Exception as e:
        traceback.print_exc()
        print()
        return -1
    return 0


def download_image_from_url(row_data, download_directory):
    try:
        imgid, flag, labelid, label, url = row_data.split(',')[:5]
    except:
        print('Row not in required format. Skipping')
        return 'pass'

    image_name = imgid + ".jpg"
    (Path(download_directory) / str(labelid)).mkdir(exist_ok=True, parents=True)
    file_name = str((Path(download_directory) / str(labelid) / image_name).expanduser())
    status = download_directory + '/' + 'status_logs/' + imgid + '.done'

    if Path(status).exists():
        pass
    else:
        try:
            req = Request(url, headers={
                "User-Agent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"})

            response = urlopen(req, None, 10)
            data = response.read()
            response.close()
            _ = resize_save_image(data, file_name, shape=(512, 512))
            #with open(file_name, 'wb') as output_file:
            #    output_file.write(data)
            with open(status, 'w') as f:
                pass
            # print("{} == > Done".format(row_id))
        except:
            status = download_directory + '/' + 'status_logs/' + imgid + '.fail'
            with open(status, 'w') as f:
                pass
            return 'fail'
    return url


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--download-directory', required=True)
    parser.add_argument('--urls-file', required=True,
                        help='tab separated file with four columns food name|url|thumbnail url')
    args = parser.parse_args()

    Path(args.download_directory).mkdir(parents=True, exist_ok=True)
    Path(args.download_directory + '/' + 'status_logs').mkdir(exist_ok=True)

    with open(args.urls_file, 'r') as f:
        id_urls = f.read().strip().split('\n')

    pbar = tqdm(id_urls)
    pool = Pool()
    for row in id_urls:
        pool.apply_async(download_image_from_url, args=(row, args.download_directory), callback=tqdmupdate)
    pool.close()
    pool.join()