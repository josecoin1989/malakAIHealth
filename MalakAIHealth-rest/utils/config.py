import configparser
import re
import os


class ConfigMalakAI:

    cfg_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "malakAI.cfg")


    def parse(self):
        self.parser = configparser.ConfigParser()
        self.parser.read(self.cfg_file)

    def get(self,section,key,defaultValue):
        if not hasattr(self, 'parser'):
            self.parse()
        val = None
        try:
            val = self.parser.get(section,key)
            # search environment variables: ${XXXXX}
            foundVal = re.match(r'\${[A-Z0-9_-]+}', val)
            if foundVal:
                foundVal = foundVal.group()
                foundVal = foundVal[2:len(foundVal) - 1]
                foundVal = os.environ[foundVal]
                val = foundVal if foundVal is not None else defaultValue
        except:
            print("FAILURE getting prop: "+section+"."+key+", return default")
        return val if val is not None else defaultValue
