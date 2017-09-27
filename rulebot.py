from slackbot.bot import respond_to
from slackbot.bot import listen_to
import re

RULEPATH = 'rules.txt'
REACTION = 'discoparrot'

@respond_to('help', re.IGNORECASE)
def help(message):
    cmds = [
            "addrule <rule>",
            "deleterule <number>",
            "rules",
            "Complaint? Make a PR: https://github.com/antitree/rulebot",
            ]
    message.reply('\n'.join(cmds))
    message.react(REACTION)


@respond_to('addrule ([a-zA-Z0-9 \'#!]*)')
def add(message, rule):
    with open(RULEPATH, 'a') as rulefile:
        rulefile.write("{}\n".format(rule))
    message.reply("Rule added")
    message.react(REACTION)
   

@respond_to('deleterule ([0-9]*)')
def delete(message, num):
    rules = _get_rules()
    output = []
    for idx, rule in enumerate(rules, 1):
        if idx != int(num):
            output.append(rule)
        else:
            message.reply("Deleting rule {}: {}".format(num, rule))
    with open(RULEPATH, 'w') as rulesfile:
        rulesfile.writelines(output)


@respond_to('rules')
def rules(message):
    rules = _get_rules()
    output = ["0: You do not talk about #opsec"]
    for num, rule in enumerate(rules, 1):
        output.append('{}: {}'.format(num, rule))
    message.send("\n".join(output))


def _get_rules():
    with open(RULEPATH, 'r') as rules:
        return rules.readlines()
