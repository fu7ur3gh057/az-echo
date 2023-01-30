from services.extract_service import ExtractService

link = 'https://news.milli.az/showbiz/1101312.html'

service = ExtractService(url=link, lang='az', negative_words=[])
text = service.start()
