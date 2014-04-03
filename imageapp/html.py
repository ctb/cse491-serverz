import os
import jinja2

template_dir = './templates'
full_template_dir = None
loader = None
env = None

def init_templates():
    global loader, env

    # calculate the location of the templates directory relative to the
    # directory this file is in
    dirname = os.path.dirname(__file__)
    t_dir = os.path.join(dirname, template_dir)
    t_dir = os.path.abspath(t_dir)

    print 'loading templates from:', t_dir
    global full_template_dir
    full_template_dir = t_dir

    loader = jinja2.FileSystemLoader(t_dir)
    env = jinja2.Environment(loader=loader)

def render(template_name, values={}):
    template = env.get_template(template_name)
    return template.render(values)

def load_file(filename):
    r = open(os.path.join(full_template_dir, filename), 'rb').read()
    return r
