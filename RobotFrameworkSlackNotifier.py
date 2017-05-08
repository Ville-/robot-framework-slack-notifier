import requests
import json
import re

class RobotFrameworkSlackNotifier:
    ROBOT_LISTENER_API_VERSION = 2
    global PASS_INDEX, NON_CRITICAL_INDEX, FAIL_INDEX, SLACK_URL_ROOT

    SLACK_URL_ROOT = "https://hooks.slack.com/services/"
    
    PASS_INDEX = 0;
    NON_CRITICAL_INDEX = 1;
    FAIL_INDEX = 2;

    def __init__(self, slack_id):
        self._init_result_object()

        self.url = SLACK_URL_ROOT + slack_id

    def _init_result_object(self):
        self.results = {}
        self.results['unfurl_links'] = True
        self.results['mrkdwn'] = True
        self.results['channel'] = "#general"
        self.results['username'] = "Robot Framework Notifier"
        self.results['icon_emoji'] = ":robot_face:"
        self.results['attachments'] = [{}, {}, {}]
        self.results['attachments'][PASS_INDEX]['fields'] = []
        self.results['attachments'][NON_CRITICAL_INDEX]['fields'] = []
        self.results['attachments'][FAIL_INDEX]['fields'] = []
        self.results['attachments'][PASS_INDEX]['color'] = "good"
        self.results['attachments'][NON_CRITICAL_INDEX]['color'] = "warning"
        self.results['attachments'][FAIL_INDEX]['color'] = "danger"
        self.results['attachments'][PASS_INDEX]['title'] = "Passed"
        self.results['attachments'][NON_CRITICAL_INDEX]['title'] = "Non-critical"
        self.results['attachments'][FAIL_INDEX]['title'] = "Failed"

    def _get_test_text(self, result):
        url = re.search("(?P<url>https?://[^\s]+)", result['doc']).group("url") if result['doc'] else ""

        if url != "":
            text = "<" + url + "|" + result['message'] + ">"
        else:
            text = result['message']

        return text

    def end_test(self, name, result):
        url = ''

        if result['status'] == 'PASS':
            test_result = self.results['attachments'][PASS_INDEX]
        elif result['critical'] == 'no':
            test_result = self.results['attachments'][NON_CRITICAL_INDEX]
        else:
            test_result = self.results['attachments'][FAIL_INDEX]

        test_result['fields'].append({
            "title": name,
            "value": self._get_test_text(result)
        })

    def end_suite(self,  name, result):
        self.results['text'] = "*" + name + "*" + "\n" + result['statistics']
        res = requests.post(self.url, data=json.dumps(self.results))


