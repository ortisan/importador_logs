import glob
import logging
import re
from datetime import datetime
from multiprocessing import Pool

from Modelos import Log
from Modelos import db
from logging.handlers import RotatingFileHandler


logger = logging.getLogger("Rotating Log")
logger.setLevel(logging.INFO)

# add a rotating handler
handler = RotatingFileHandler("./logs/logProcessamento.log", maxBytes=4194304,
                              backupCount=50)
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

logger.addHandler(handler)


# logging.basicConfig(filename='processamentoLogs.log', level=logging.DEBUG,
#                     format='%(asctime)s %(levelname)s:%(message)s')


# '177.148.225.122 - - 19/Nov/2015:15:20:14 -0200 GET /AppsGratisUpdate.json HTTP/1.1 200 179 - Mozilla/5.0 (X11 Ubuntu Linux x86_64 rv:42.0) Gecko/20100101 Firefox/42.0'
# 352e27de85af2f774fc2b2e9b716796fb72cda88ea1fce223916b294ee74d477 drop.mundopositivo.com.br [27/Nov/2015:13:47:46 +0000] 186.231.142.6 - 51511B9E8ECDB47C REST.GET.OBJECT AppGratis_1.0.39b1_versionCode_39_atualizar_assinado_merge_adaptacoes_lollipop.apk "GET /drop.mundopositivo.com.br/AppGratis_1.0.39b1_versionCode_39_atualizar_assinado_merge_adaptacoes_lollipop.apk HTTP/1.1" 200 - 3352871 3352871 112 88 "-" "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:42.0) Gecko/20100101 Firefox/42.0" -


def import_log(file):
    with open(file) as f:
        logger.info('Processando arquivo: %s ...' % (str(f)))

        with db.atomic():

            logs = []

            for line in f:
                if re.search('lollipop.apk', line):
                    try:
                        line = re.sub(r'[\[||\]|\n|\"|\'|\;\,]+', '', line)
                        fields = line.split(' ')
                        id = '%s%s' % (fields[0], fields[6])
                        ip = fields[4]

                        date_temp = fields[2]
                        import time
                        data = datetime.strptime(date_temp, "%d/%b/%Y:%H:%M:%S")
                        status = fields[12]
                        method = fields[9]
                        url = fields[10]
                        dados_device = " - ".join(fields[11:])

                        logs.append(
                                {'id': id, 'ip': ip, 'data': data, 'method': method, 'status_code': status, 'url': url,
                                 'dados_device': dados_device})

                        # log = Log(id=id, ip=ip, data=data, method=method, status_code=status, url=url,
                        #           dados_device=dados_device)
                        #
                        # log.save()
                    except BaseException as exc:
                        logger.error("Erro ao processar linha %s ..." % (line))

            try:
                Log.insert_many(logs).execute()
            except BaseException as exc:
                logger.error("Erro ao processar linha %s ..." % (line))

            logger.info('Terminando processamento do arquivo: %s ...' % (str(f)))

    return True


if __name__ == '__main__':
    import multiprocessing
    processors = multiprocessing.cpu_count()

    p = Pool(processors)
    dirs = ['/home/marcelo/Documents/logs/logs/']
    for dir in dirs:
        p.map(import_log, glob.glob(dir + '*'))
