import json
import subprocess
import os
from datetime import datetime, date

from file_model import FileModel

class JsonParser: 
    exiftool_exe = os.getcwd() + os.sep + "binary" + os.sep + "exiftool" + os.sep + "exiftool.exe"
    date_format = '%m-%d-%Y'

    def parseFile(fileModel: FileModel):
        with open(fileModel.json_file, 'r', encoding='utf8') as json_file:
            try:
                content = '\r'.join(json_file.readlines())
                json_file.close()
                return json.loads(content)
            except json.JSONDecodeError as e:
                json_file.close()
                return ParseAttributes.extractData(fileModel)


    def parseDate(json_object: json, file_name: str):
        parsed_date = JsonParser.parseJsonDate(json_object, 'DateTimeOriginal')
        if parsed_date != None:
            return parsed_date
        dates = []
        for item in json_object:
            for element in item:
                if 'date' in str(element).lower():
                    parsed_date = JsonParser.parseJsonDate(json_object, element)
                    if parsed_date != None:
                        if parsed_date < date(2000, 1, 1): 
                            continue
                        if parsed_date.strftime("%Y") in file_name and parsed_date < date(2024, 1, 1):
                            return parsed_date
                        dates.append(parsed_date)
        return sorted(dates, reverse=False)[0]

    def parseJsonDate(json_object: json, element: str):
        try:
            return datetime.strptime(JsonParser.parseData(json_object, element), JsonParser.date_format).date()
        except:
            return None

    def exportJson(source_file: str, json_file: str):
        exiftool_command = [
            JsonParser.exiftool_exe, 
            source_file, 
            '-d', 
            JsonParser.date_format, 
            '-json', 
            '-W+!', 
            json_file]
        subprocess.run(exiftool_command)

    def parseData(json_object: json, key: str):
        try:
            if isinstance(json_object, list):
                return json_object[0][key]
            else:
                return json_object[key]
        except:
            return None
        

from PIL import Image, ExifTags
from datetime import datetime
import exifread

class ParseAttributes: 
    date_format = '%Y:%m:%d %H:%M:%S'

    def extractData(fileModel: FileModel):
        # with open(fileModel.source_file, 'rb') as fh:
        #     tags = exifread.process_file(fh)
        #     print(ParseAttributes.getValue(tags, 'EXIF DateTimeOriginal'))
        #     print(ParseAttributes.getValue(tags, 'EXIF DateTimeDigitized'))
        #     print(ParseAttributes.getValue(tags, 'EXIF DateTimeOriginal'))
        #     print(ParseAttributes.getValue(tags, 'Image DateTime'))

        image = Image.open(fileModel.source_file)
        exif_metadata = image.getexif()
        image.close()
        if exif_metadata is not None:
            data = {}
            data['DateTimeOriginal'] = datetime.strptime(ParseAttributes.getPropertyValue(exif_metadata, 'DateTime'), ParseAttributes.date_format).date()
            data['FileSize'] = image.size
            data['XResolution'] = ParseAttributes.getPropertyValue(exif_metadata, 'XResolution')
            data['YResolution'] = ParseAttributes.getPropertyValue(exif_metadata, 'YResolution')
            return json.dumps(data)

    def getPropertyValue(exif_metadata, property: str):
        for key, val in exif_metadata.items():
            if key in ExifTags.TAGS:
                if ExifTags.TAGS[key] == property: 
                    return val

    def getValue(tags, name):
        return tags[name]
