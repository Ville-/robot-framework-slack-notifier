import requests
import json
import re

class RobotFrameworkSlackNotifier:
    ROBOT_LISTENER_API_VERSION = 2

    SLACK_URL_ROOT = "https://hooks.slack.com/services/"

    PASS_INDEX = 0;
    NON_CRITICAL_INDEX = 1;
    FAIL_INDEX = 2;

    def __init__(self, slack_id, channel='#general', show_documentation=True):
        self.url = self.SLACK_URL_ROOT + slack_id
        self.show_documentation = show_documentation
        self.channel = channel

        self._init_slack_message()

    def _init_slack_message(self):
        self.slack_message = {}
        self.slack_message['unfurl_links'] = False
        self.slack_message['mrkdwn'] = True
        self.slack_message['channel'] = self.channel
        self.slack_message['username'] = "Robot Framework Notifier"
        self.slack_message['icon_emoji'] = ":robot_face:"

        self.slack_message['attachments'] = [{}, {}, {}]
        self._init_attachment(self.PASS_INDEX, 'Passed', 'good')
        self._init_attachment(self.NON_CRITICAL_INDEX, 'Non-Critical', 'warning')
        self._init_attachment(self.FAIL_INDEX, 'Failed', 'danger')

    def _init_attachment(self, index, title, color):
        self.slack_message['attachments'][index]['fields'] = []
        self.slack_message['attachments'][index]['title'] = title
        self.slack_message['attachments'][index]['color'] = color

    def end_test(self, name, result):
        url = ''

        if result['status'] == 'PASS':
            test_result = self.slack_message['attachments'][self.PASS_INDEX]
        elif result['critical'] == 'no':
            test_result = self.slack_message['attachments'][self.NON_CRITICAL_INDEX]
        else:
            test_result = self.slack_message['attachments'][self.FAIL_INDEX]

        test_result['fields'].append({
            "title": name,
            "value": result['message']
        })

    def end_suite(self,  name, result):
        self.slack_message['text'] = "*" + name + "*" + "\n"
        self.slack_message['text'] += result['statistics']
        if self.show_documentation:
            self.slack_message['text'] +=  "\n" + result['doc']

        requests.post(self.url, data=json.dumps(self.slack_message))


