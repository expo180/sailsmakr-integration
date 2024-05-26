# app/filters.py

def mask_token(token):
    if len(token) > 3:
        return '*' * (len(token) - 3) + token[-3:]
    return token

def register_filters(app):
    app.jinja_env.filters['mask_token'] = mask_token
