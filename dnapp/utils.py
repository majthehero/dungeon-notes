from flask import current_app as app


def parse_players(players: str):
    emails = players.split(",")
    valid_emails = []
    for email in emails:
        if len(email) < 3:
            continue
        if "@" not in email:
            continue
        valid_emails.append(email.strip())
    app.logger.warn("valid emails: %s", valid_emails)
    return valid_emails
