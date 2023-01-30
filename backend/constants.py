REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/35.0.1916.47 Safari/537.36'
}

NEGATIVE_EXTENSIONS = [
    ".mp4",
    ".mp3",
    ".pdf",
    ".jpg",
    ".jpeg",
    ".png",
    ".flv",
    ".csv",
    ".docx",
    ".xml",
    ".xlsx",
    ".svg",
    ".pptx"
]

NEGATIVE_SITES = [
    'facebook.com/',
    'instagram.com/',
    'www.google.com/',
    't.me/',
    'twitter.com/',
    'vk.com/',
    'wiki.com/',
    'youtube.com/',
    'ok.ru/',
    'gmail.ru/',
    'yandex.ru/',
    'whatsapp.com/',
    'play.google.com',
    'itunes.apple.com',
]

NEGATIVE_DOMAINS = [
    'wiki',
    'wikiquote',
    'wikia',
    'wikihow',
    'wiktionary',
    'wikimedia',
    'wikibooks',
    'wikimapia',
    'youtube',
    'youtu',
    'instagram',
    'facebook',
    'fb',
    'ask',
    'twitter',
    'reddit',
    'telegram',
    't',
    'google',
    'spotify',
    'vk',
    'vkontakte',
    'ok',
    'linkedin',
    'amazon',
    'ebay',
    'paypal',
    'mail',
    'gmail',
    'pinterest',
    'netflix',
    'baidu',
    'rambler',
    'whatsapp',
    'wechat',
    'yandex',
    'yahoo',
    'apple',
    'twitch',
    'wa',
    'istockphoto'
]

VOICE_CHOICES = (
    (325640, 'Aytac, AZ, female'),
    (325641, 'Aynur, AZ, female'),
    (325642, 'Ramin, AZ, male'),
    (325643, 'Elchin, AZ, male'),
    (325648, 'Kamil, AZ, male'),
    (325647, 'Zeynep, TR, female'),
    (325646, 'Mesut, TR, male'),
    (325644, 'Sibel, TR, female'),
    (325645, 'Anna, RU, female'),
)

# Periodic tasks priority
DISCOVER_PRIORITY = 5
EXTRACT_PRIORITY = 5
DRILLER_PRIORITY = 3
GENERATOR_PRIORITY = 8
EMAIL_PRIORITY = 10
SUBSCRIPTION_CHECKER_PRIORITY = 9
