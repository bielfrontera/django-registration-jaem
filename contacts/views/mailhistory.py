# coding: utf-8

from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponseForbidden, HttpResponseServerError, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, render
from django.template import RequestContext
from django.utils import simplejson
from django.utils.html import escape
from datetime import date, datetime, timedelta

from django.conf import settings
from contacts.models import Person
from email.header import decode_header
from email.utils import parsedate_tz,mktime_tz

import imaplib, email, re
from django.utils.translation import ugettext as _


list_response_pattern = re.compile(r'\((?P<flags>.*?)\) "(?P<delimiter>.*)" (?P<name>.*)')


def parse_list_response(line):
    """ Parse '(\\HasNoChildren) "/" "INBOX"'
    FROM: http://www.doughellmann.com/PyMOTW/imaplib/
    """
    flags, delimiter, mailbox_name = list_response_pattern.match(line).groups()
    mailbox_name = mailbox_name.strip('"')
    return (flags, delimiter, mailbox_name)

def get_mail_history(email_address):

    mail_client = imaplib.IMAP4_SSL(settings.EMAIL_IMAP_HOST)
    mail_client.login(settings.EMAIL_HOST_USER , settings.EMAIL_HOST_PASSWORD)

    if mail_client.state != "AUTH":
        raise Exception (_('Mail login incorrect'))

    # cercam Inbox i All Mail
    inbox_folder = 'INBOX'
    sent_folder = ''
    allmail_folder = ''

    for mail_folder in mail_client.list()[1]:
        flags, delimiter, mailbox_name = parse_list_response(mail_folder)
        if mailbox_name.lower().find('sent') != -1 or flags.lower().find('sent') != -1:
            sent_folder = mailbox_name
        if flags.lower().find('all') != -1:
            allmail_folder = mailbox_name

    if allmail_folder != '':
        mail_client.select(allmail_folder)
        result, message_ids = mail_client.search(None, '(OR (TO "%s") (FROM "%s"))' % (email_address,email_address))
    else:
        # Cercam tant a inbox com a sent
        mail_client.select(inbox_folder)
        result, message_ids_received = mail_client.search(None, '(FROM "%s")' % email_address)
        if sent_folder != '':
            mail_client.select(sent_folder)
            result, message_ids_sent = mail_client.search(None, '(TO "%s")' % email_address)
            #merge de les dues llistes
            message_ids = [''.join(message_ids_received[0]+message_ids_sent[0])]
        else:
            message_ids = message_ids_received

    messages = []
    for message_id in message_ids[0].split():
        result,message_string = mail_client.fetch(message_id, "(RFC822)")
        messages.append(email.message_from_string(message_string[0][1]))

    mail_client.logout()
    return messages

def get_message_body(message):
    for part in message.walk():
        if part.get_content_type() == 'text/plain':
            body = part.get_payload()
            if len(body) > 250:
                body = body[0:250] + ' (...)'
            return body
    return None

def decode_message_header(header):
    result_header, encoding = decode_header(header)[0]
    try:
        return result_header.decode(encoding)
    except:
        return header

def get_message_date(msg_date):
    date_utc = mktime_tz(parsedate_tz(msg_date))
    return datetime.fromtimestamp(date_utc).strftime('%Y-%m-%dT%H:%M:%S')

def mail_history(request, id):
    """Fetch mail history of a contact

    :param id: contact id.
    """
    results = []

    if not request.user.is_authenticated():
        results = {'error' : True, 'error_message' : _('User is not authenticated')}
        json = simplejson.dumps(results)
        return HttpResponse(json, mimetype='application/json')
    try:
        person = Person.objects.get(id=id)
    except Person.DoesNotExist:
        results = {'error' : True, 'error_message' : _('Person does not exist in database')}
        json = simplejson.dumps(results)
        return HttpResponse(json, mimetype='application/json')

    try:
        result_messages = get_mail_history(person.email_address)
    except Exception as e:
        results = {'error' : True, 'error_message' : str(e)}
        json = simplejson.dumps(results)
        return HttpResponse(json, mimetype='application/json')

    results = {'error' : False, 'messages' : [ {'from' : decode_message_header(message['From']), 'subject': decode_message_header(message['Subject']),'date': get_message_date(message['Date']),'body' : get_message_body(message) } for message in result_messages ]}
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')
