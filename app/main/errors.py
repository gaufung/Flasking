from flask import render_template, request, jsonify

from . import main

@main.app_errorhandler(404)
def page_not_found(e):
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        respone = jsonify({'error':'not found'})
        respone.status = 404
        return respone
    return render_template('404.html'), 404

@main.app_errorhandler(500)
def internel_server_error(e):
    return render_template('500.html'), 500