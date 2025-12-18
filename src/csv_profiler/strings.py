def slugify(text: str)->str:
    '''trun 'report name' -> 'report-name' '''
    return text.casefold().replace(" ","-").strip()


