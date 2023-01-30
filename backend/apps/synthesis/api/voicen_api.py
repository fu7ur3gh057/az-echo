import requests
import json

VOICEN_ACCESS_TOKEN = 'cbbd932a-87d9-475f-9000-3a462bec1946'
VOICEN_TTS_URL = 'https://tts.voicen.com/api/v1/jobs'


def post_synthesis(text: str, lang: str):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Token {VOICEN_ACCESS_TOKEN}',
    }
    if lang == 'az':
        voice_id = "325652"
    else:
        voice_id = "325645"
    send_data = {"text": text, "lang": lang, "voice_id": voice_id}
    response = requests.post(
        f'{VOICEN_TTS_URL}/text/',
        headers=headers,
        data=json.dumps(send_data)).json()
    data = response['data']
    return data['id']


def check_synthesis_status(job_id):
    headers = {
        'Authorization': f'Token {VOICEN_ACCESS_TOKEN}',
    }
    response = requests.get(f'{VOICEN_TTS_URL}/{job_id}/', headers=headers).json()
    data = response['data']
    status = data['status']
    if status == 'ready' or status == 'failed':
        return True
    else:
        return False


def get_synthesis_audio(job_id):
    headers = {
        'Authorization': f"Token {VOICEN_ACCESS_TOKEN}",
    }
    response = requests.get(f'{VOICEN_TTS_URL}/{job_id}/synthesize/', headers=headers)
    if response.status_code == 200:
        return response.content
    else:
        raise Exception('Error')
