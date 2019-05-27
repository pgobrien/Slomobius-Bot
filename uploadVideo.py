import os
import uuid
import pysftp
import pfycat

from gfycat.client import GfycatClient

class NoNSFWException(Exception):
    pass


class vidUpload(object):

    def __init__(self, user_agent, debug, dryrun):

        import mysecret

        self.dryrun = dryrun
        self.debug = debug

        self.gfyclient = GfycatClient()

        self.pycatclient = pfycat.Client()


        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None
        self.ixny = {
            'host':mysecret.ixni_host,
            'user':mysecret.ixni_user,
            'pass':mysecret.ixni_pass,
            'cnopts':cnopts}


    def __call__(self, file_name, over_18):
        return self.upload_file(file_name, over_18)


    def upload_file_gfycat(self, locale_file_name):
        r = self.pycatclient.upload(locale_file_name)
        return "https://gfycat.com/" + r["gfyname"]


    def upload_file_insxnity(self, locale_file_name):

        srv = pysftp.Connection(
            host=self.ixny['host'],
            username=self.ixny['user'],
            password=self.ixny['pass'],
            cnopts=self.ixny['cnopts']
        )

        with srv.cd('/var/www/html/slowmobiushost'):
            srv.put(locale_file_name)


        srv.close()

        return "myfilestorage.com/" + os.path.basename(locale_file_name)


    def upload_file(self, locale_file_name, over_18):

        oldext = os.path.splitext(locale_file_name)[1]
        newName = str(uuid.uuid4()) + oldext
        os.rename(locale_file_name, newName)


        if self.dryrun:
            print("DryRun")



        try:
            return self.upload_file_gfycat(newName)
        except Exception as e:
            print("gfycat-error: ", e.__class__, e.__doc__)



        try:
            return self.upload_file_insxnity(newName)
        except Exception as e:
            print("Server upload Fail: ", e.__class__, e.__doc__)











































