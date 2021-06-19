from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for, \
                  abort, jsonify, render_template_string

import re

mod = Blueprint('core', __name__)

@mod.route('/')
def level1():
  name = request.args.get('name')
  if name is None:
    return redirect(url_for('core.level1') + '?name=FirstName')
  if '<' in name:
    if re.search(r'<(?!(input|/input))', name):
        return 'Only &lt;input&gt; tag is allowed', 403
    if 'onclick' in name or 'onmouse' in name or 'onload' in name or 'onfocus' in name:
      return 'Event handlers are not allowed', 403
  return (render_template('core/index.html', nav='index', name=name))