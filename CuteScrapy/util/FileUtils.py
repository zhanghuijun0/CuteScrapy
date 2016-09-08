def writeMetaFile(self, response):
    filename = response.url.split("/")[-1]
    print filename
    if 'htm' not in filename:
        filename = filename + '.html'
    with open('../files/' + filename, 'wb') as f:
        f.write(response.body.replace('charset=gb2312', 'charset=utf8'))