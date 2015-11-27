from Modelos import Log
import glob
import csv


# '177.148.225.122 - - 19/Nov/2015:15:20:14 -0200 GET /AppsGratisUpdate.json HTTP/1.1 200 179 - Mozilla/5.0 (X11 Ubuntu Linux x86_64 rv:42.0) Gecko/20100101 Firefox/42.0'

def importt(dir="/home/marcelo/Documents/logs-update/logs-appen-1/"):
    # with open('acessos.csv', 'wb') as csvfile:
    # spamwriter = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)

    for f_str in glob.glob(dir + 'http-deskmedia-access.log*'):
        with open(f_str) as f:

            print ("processando arquivo: ", f)

            for line in f:
                import re

                if not re.search('AppsGratisUpdate.json', line):
                    continue

                try:
                    line = re.sub(r'[\[||\]|\n|\"|\'|\;\,]+', '', line)
                    fields = line.split(' ')
                    ip = fields[0]

                    date_temp = fields[3]
                    m = re.search(r'(\d+\/\w+\/\d+)\:(\d+\:\d+\:\d+)', date_temp)
                    date_str = m.group(1)
                    hour = m.group(2)
                    import time
                    from datetime import datetime
                    date = datetime.strptime(date_temp, "%d/%b/%Y:%H:%M:%S")
                    status_code = fields[4]
                    method = fields[5]
                    url = fields[6]
                    device = " - ".join(fields[11:])

                    log = Log(ip=ip, data=date, method=method, status_code=status_code, url=url,
                              dados_device=device)
                    log.save()

                    # spamwriter.writerow([ip, date_str, hour, url, device])
                except BaseException as exc:
                    print exc


if __name__ == '__main__':
    importt(dir='/home/marcelo/Documents/logs-update/logs-appen-1/')
    importt(dir='/home/marcelo/Documents/logs-update/logs-appen-2/')
    importt(dir='/home/marcelo/Documents/logs-update/logs-appen-3/')
