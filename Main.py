import glob
import re
import concurrent.futures
from Modelos import Log
from datetime import timedelta
from datetime import datetime
import hashlib


# '177.148.225.122 - - 19/Nov/2015:15:20:14 -0200 GET /AppsGratisUpdate.json HTTP/1.1 200 179 - Mozilla/5.0 (X11 Ubuntu Linux x86_64 rv:42.0) Gecko/20100101 Firefox/42.0'

def importt(dir):
    for f_str in glob.glob(dir + 'http-deskmedia-access.log*'):
        with open(f_str) as f:
            with open('processamento.log', 'w') as fl:
                fl.write('processando arquivo: %s ...\n' %(str(f)))  # python will convert \n to os.linesep

            # with concurrent.futures.ThreadPoolExecutor(max_workers=0) as executor:
            #     executor.map(process_line, f)

            for line in f:
                process_line(line)


def process_line(line):
    if not re.search('AppsGratisUpdate.json', line):
        return

    try:
        line = re.sub(r'[\[||\]|\n|\"|\'|\;\,]+', '', line)
        fields = line.split(' ')
        ip = fields[0]

        date_temp = fields[3]
        # m = re.search(r'(\d+\/\w+\/\d+)\:(\d+\:\d+\:\d+)', date_temp)
        # date_str = m.group(1)
        # hour = m.group(2)
        import time
        data = datetime.strptime(date_temp, "%d/%b/%Y:%H:%M:%S")
        status = fields[4]
        method = fields[5]
        url = fields[6]
        dados_device = " - ".join(fields[11:])
        timestamp = time.mktime(data.timetuple())

        m = hashlib.md5()
        m.update('%s_%d_%s' % (ip, timestamp, dados_device))
        id = m.hexdigest()


        log = Log(id=id, ip=ip, data=data, method=method, status_code=status, url=url,
                  dados_device=dados_device)
        log.save(force_insert=True)

        # spamwriter.writerow([ip, date_str, hour, url, device])
    except BaseException as exc:
        print exc


if __name__ == '__main__':
    importt(dir='/home/marcelo/Documents/logs-update/logs-appen-1/')
    importt(dir='/home/marcelo/Documents/logs-update/logs-appen-2/')
    importt(dir='/home/marcelo/Documents/logs-update/logs-appen-3/')
