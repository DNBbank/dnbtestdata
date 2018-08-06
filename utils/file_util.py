import codecs
import datetime
import json

from utils.date_util import DateUtil


class FileUtil:
    @classmethod
    def json_to_json_file(cls, some_json, name):
        filename = cls._filename_json_string(name)
        try:
            print(json.dumps(some_json, indent=2, ensure_ascii=False))
        except TypeError as e:
            print("typeError: " + e)
            raise

        with codecs.open(filename, 'w', encoding='utf-8') as outfile:
            json.dump(some_json, outfile, ensure_ascii=False)

    @classmethod
    def _filename_json_string(cls, name):
        return name + '-' + DateUtil.date_string(datetime.date.today()) + '.json'
