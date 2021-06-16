from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for, \
                  abort, jsonify, render_template_string

import re

mod = Blueprint('core', __name__)

@mod.route('/')
def level1():
  name = request.args.get('name')
  if name is None:
    return redirect(url_for('core.level1') + '?name=FirstName')
  original = name
  # block all script tags
  name = name.replace('<script', '')
  # block alert function
  # name = name.replace('alert(', '')
  # block all other tags with malicious attributes
  # name = re.sub(r' on[a-zA-Z]+\=', '', name)
  print(original, name)
  return (render_template('core/index.html', nav='index', name=name))