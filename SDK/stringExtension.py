class StringExtension(str):
    def splitAndStrip(self, delimeter):
        return [x.strip() for x in self.split(delimeter)]