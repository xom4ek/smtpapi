from smtplib import SMTP
from smtplib import SMTP_SSL
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging
import time

LOGGER = logging.getLogger(__name__)

class smtpwrapper():
    class Email(MIMEMultipart):
        def __init__(self,to,From,body,subject,*args,**kwargs):
            super().__init__(*args,**kwargs)
            self['Subject'] = subject
            self['From'] =  From
            self['To'] =  to
            self.attach(MIMEText(body,'html'))
            LOGGER.debug('Message Body: %s' % body)
            LOGGER.debug('Message To: %s' % to)
            LOGGER.debug('Message From: %s' % to)
            LOGGER.debug('Message Subject: %s' % subject)

    def __init__(self,hostname,port,username,password,try_max=5,use_tls=True,*args,**kwargs):
        self.username=username
        self.password=password
        self.hostname=hostname
        self.port= port
        self.password = password
        self.try_cnt=0
        self.try_max=try_max
        self.try_delay=0
        self.use_tls=use_tls
        try:
            self.conn=self.create_conn
        except Exception as e:
            LOGGER.error(e.__str__())

    def maybe_reconnect(self,conn):
        try:
            self.reconnect = conn.noop()[0]
        except Exception as e:
            LOGGER.error(e.__str__())
            self.reconnect = -1
        return True if self.reconnect == 250 else False

    def get_delay(self):
            if self.try_cnt == 1:
                self.try_delay = 5
            else:
                self.try_delay += 5
            if self.try_delay > 30:
                self.try_delay = 30
            return self.try_delay

    def create_conn(self):
        LOGGER.info('Connecting to %s' % self.hostname)
        if self.use_tls:
            res = self.conn = SMTP_SSL(host=self.hostname,port=self.port)
            LOGGER.info(res)
        else:
            self.conn = SMTP()
            res = self.conn.connect(self.hostname,self.port)
            LOGGER.info(res)
        try:
            log = self.conn.login(self.username,self.password)
            LOGGER.info(log)
        except Exception as e:
            LOGGER.error(e.__str__())
            self.try_cnt=self.try_cnt+1
            LOGGER.info('Try_cnt %s' % self.try_cnt)
            try_delay = self.get_delay()
            LOGGER.info('Try_delay %s' % try_delay)
            time.sleep(try_delay)
            if self.try_cnt < self.try_max:
                self.create_conn()
            else:
                return Exception
        return self.conn

    def send_email(self,msg):
        self.try_cnt=0
        if not self.maybe_reconnect(self.conn):
            LOGGER.info('Start reconnect')
            self.conn = self.create_conn()
        else:
            LOGGER.info('Use existing connection')
        try:
            LOGGER.info('Start send message')
            result = self.conn.send_message(msg)
            return self,result
        except Exception as e:
            LOGGER.error(e.__str__())
            return self,e
    def sendTemplate(self,*args,**kwargs):
        msg=self.Email(**kwargs)
        return self.send_email(msg)

if __name__ == "__main__":
    import yaml
    class Struct:
        def __init__(self, **entries):
            self.__dict__.update(entries)

    def Get_config(config):
        with open(config) as f:
            return Struct(**yaml.safe_load(f))
    logging.basicConfig(level=logging.DEBUG)
    cfg=Get_config('config.yml')
    LOGGER.debug(cfg.smtp)
    smtp = smtpwrapper(**cfg.smtp)
    smtp , result = smtp.sendTemplate(**cfg.send,subject='Privet 1')
    smtp , result = smtp.sendTemplate(**cfg.send,subject='Privet 2')
    smtp , result = smtp.sendTemplate(**cfg.send,subject='Privet 3')
    LOGGER.debug('%s' % (result))
