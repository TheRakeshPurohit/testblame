# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import os
import sendgrid
from sendgrid.helpers.mail import Content, Email, Mail
import re


def send_email(from_email, to_email, subject, content):
    try:
        sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('+'))
        from_email = Email(from_email)
        to_email = Email(to_email)
        content = Content("text/html", content)
        mail = Mail(from_email, subject, to_email, content)
        response = sg.client.mail.send.post(request_body=mail.get())
    except Exception as err:
        print(err)


def save_email_content(html):
    # open file with *.html* extension to write html
    file = open("email.html", "w")
    # write then close file
    file.write(html)
    file.close()


def make_tests_linkable(test_list, url):
    """This function make test linkable and very specific to
    robottelo test suite.
    """
    test_list_links = ''
    for test in test_list:
        test_split = test.split('.')
        test_link = '</br><a href="{0}{1}/{2}/{3}" target="_blank">{4}</a></br>'. \
            format(url, '.'.join(test_split[:-2]), "".join(test_split[-2:-1]),
                   "".join(test_split[-1:]), test)
        test_list_links += test_link
    return test_list_links


def build_content(tests, jenkins_url, with_link):
    with open('email_template', 'r') as myfile:
        email_content = myfile.read()
    if isinstance(tests, dict):
        for author, test_list in tests.items():
            if '@' in author:
                author = re.findall("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", author)[0]
            author_col = "<tr><td>{0}</td>".format(author)
            if with_link is None:
                table = author_col + "<td class=myclass>"+"<br/><br/>".join(test_list)
            else:
                test_col = "<td class=myclass>"
                table = author_col + test_col + make_tests_linkable(test_list, jenkins_url)
            email_content = email_content + table + "</td></tr>"
    email_content = email_content + "</table></body></html>"
    save_email_content(email_content)
    return email_content
