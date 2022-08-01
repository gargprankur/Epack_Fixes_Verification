import  xml.etree.ElementTree as ET

class UcodeFixes:
        def __init__(self, file_name):
                root = ET.parse(file_name)
                count_temp_fixes = root.find('.//temporary_patches')
                self._fixes = []
                print(count_temp_fixes.text)
                for patches in root.findall('.//Patch'):
                        fix_type = patches.find('.//type')
                        if fix_type.text == 'Temp':
                                fix_number = patches.find('.//number')
                                self._fixes.append(int(fix_number.text))


        @property
        def fixes(self):
                return self._fixes