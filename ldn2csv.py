import argparse
import csv
import glob
import logging
import os
import tarfile
import tempfile
import time
import re
import urllib.error
import urllib.request
from contextlib import contextmanager
from typing import Optional

logger = logging.getLogger(__name__)


def main(outfilepath: Optional[str] = 'livedoornews.csv'):
    """livedoor ニュースコーパスをcsvファイルで取得

    Parameters
    ----------
    outfilepath : str, optional
        出力ファイルパス, by default 'livedoornews.csv'

    Notes
    ----------
    ライセンスは出典元を確認してください。
    https://www.rondhuit.com/download.html#ldcc
    """

    url = 'https://www.rondhuit.com/download/ldcc-20140209.tar.gz'
    out = 'livedoornews.csv' if not outfilepath else outfilepath
    try:
        with tempfile.TemporaryDirectory() as tmp_dir:
            # livedoor newsコーパス取得
            logger.info('Start Downloading.')
            local_filename, headers = urllib.request.urlretrieve(url)
            logger.info('successful download.')
            # tar.gz解凍
            logger.info('Start decompressing tar.gz.')
            with tarfile.open(local_filename) as tar:
                tar.extractall(tmp_dir)
            logger.info('Successfully decompressed tar.gz.')
            # 対象ファイル群取得
            read_fp = os.path.join(tmp_dir, 'text', '**', '*.txt')
            reg_ignore = re.compile('license', re.IGNORECASE)
            files = [rf for rf in glob.glob(read_fp)
                     if not reg_ignore.search(os.path.basename(rf))]
            # csvファイル書き込み
            with open(out, 'w', encoding='utf-8-sig', newline='') as of:
                writer = csv.writer(of)
                ls_header = ['url', 'datetime', 'title', 'body', 'media']
                writer.writerow(ls_header)
                # 対象ファイルを読み込みcsvの1行に格納
                media_name = ''
                for read_file in files:
                    dir_name, base_name = os.path.split(read_file)
                    if media_name != os.path.basename(dir_name):
                        media_name = os.path.basename(dir_name)
                        logger.info(
                            'Start to convert format.: {}.'.format(media_name))
                    ls_row = []
                    try:
                        with open(read_file, 'r', encoding='utf-8', newline='') as rf:
                            for _ in range(3):
                                # url,datetime,titleを取得
                                ls_row.append(next(rf).strip())
                            # bodyを取得
                            ls_row.append('\n'.join(line.strip()
                                                    for line in rf if line.strip()))
                            # mediaを取得
                            ls_row.append(media_name)
                            writer.writerow(ls_row)
                    except Exception as ex:
                        # 読み込みエラーのログ
                        logger.error(
                            '{} reading failed. {}'.format(base_name, ex))
    except Exception as ex:
        logger.error(ex)
    return None


@contextmanager
def timer(name: str, logger: Optional[logging.Logger] = None):
    """
    with文で使うとwithブロック内の計算の実行時間を測ってくれる。
    以下よりコピペした：
    https://qiita.com/kaggle_master-arai-san/items/d59b2fb7142ec7e270a5?utm_campaign=popular_items&utm_medium=feed&utm_source=popular_items

    Examples
    --------
    >>> def wait(sec: float):
    >>>     time.sleep(sec)
    >>>
    >>> with timer("wait"):
    >>>     wait(2.0)
    [wait] done in 2 s

    """
    t0 = time.time()
    yield
    msg = f'[{name}] done in {time.time()-t0:.0f} s'
    if logger:
        logger.info(msg)
    else:
        print(msg)


def get_logger(setlevel=logging.INFO, logfilepath: Optional[str] = None):
    """log出力用のlogger設定用関数.

    Parameters
    ----------
    logfilepath : str, optional
        ファイルに出力したい場合はパスを指定
    """
    logFormatter = logging.Formatter(
        '%(asctime)s [%(threadName)s] - %(levelname)s - %(message)s')
    rootLogger = logging.getLogger()
    rootLogger.setLevel(setlevel)

    if logfilepath:
        fileHandler = logging.FileHandler(logfilepath)
        fileHandler.setFormatter(logFormatter)
        rootLogger.addHandler(fileHandler)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    rootLogger.addHandler(consoleHandler)
    return rootLogger


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='livedoor ニュースコーパスを取得しcsvで保存します')
    parser.add_argument(
        '--output',
        '-o',
        help='出力したいcsvファイルパス',
        type=str,
        default='livedoornews.csv')
    parser.add_argument(
        '--logfile',
        '-lf',
        help='logをファイル出力したい場合のファイルパス',
        type=str)
    args = parser.parse_args()

    logger = get_logger(logfilepath=args.logfile)
    with timer('main', logger):
        main(args.output)
