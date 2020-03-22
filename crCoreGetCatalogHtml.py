# 3rd
from yattag import Doc  # Generate HTML

# My
from crLogHeader import *
from crLocaleHeader import *

# Read these code from bottom to top is suggested
#
# Module scope config
environment_config_local = None
message_config_local = None

# Empty HTML template
#
# doc, tag, text = Doc().tagtext()
# doc.asis("<!DOCTYPE html>")
# with tag("html"):
#     with tag("head"):
#         doc.stag("meta", charset="utf-8")
#         with tag("title"):
#     with tag("body"):
#         with tag("p"):

# Format system language to HTML language


def _get_html_language():
    return get_system_language().replace('_', '-')

# Convert catalog node to HTML object rescue

# This code example comes from
# https://www.w3schools.com/howto/howto_js_treeview.asp


def _process_catalog_node(catalog_node, doc, tag, text):
    # A catalog node have two status
    if catalog_node.have_sub_node == False:
        # li with no_sub_node class
        with tag("li", klass="catalog_node no_sub_node"):
            # Name
            with tag("summary", klass="catalog_node_name"):
                # Url
                text(catalog_node.catalog_name)
    #
    # else if catalog_node.have_sub_node == True:
    else:
        # li with have_sub_node class
        with tag("li", klass="catalog_node have_sub_node"):
            # Name
            with tag("summary", klass="catalog_node_name"):
                # Url
                text(catalog_node.catalog_name)
            # Create its sub-node
            with tag("ul", klass="catalog_sub_node_list"):
                for child in catalog_node.sub_node_list:
                    _process_catalog_node(child, doc, tag, text)


# Wrap, convert catalog node object to HTML text


def get_catalog_html_text(catalog_node):
    global message_config_local

    doc, tag, text = Doc().tagtext()
    doc.asis("<!DOCTYPE html>")
    with tag("html", lang=_get_html_language()):

        # Head & Meta
        with tag("head"):
            doc.stag("meta", charset="utf-8")
            # Title
            with tag("title"):
                text(catalog_node.catalog_name +
                     message_config_local['html_catalog']['title'])
            # CSS
            doc.stag("link", rel="stylesheet",
                     href=environment_config_local['data_catalog']['css_file_name'])
            # JavaScript
            with tag("script", type="text/javascript", src=environment_config_local['data_catalog']['js_file_name']):
                text("")

        # Body & onLoad method
        with tag("body", onLoad="catalogOnLoad()"):
            with tag("div"):
                _process_catalog_node(catalog_node, doc, tag, text)

    return doc.getvalue()

# Receive config


def init_core_get_catalog_html(environment_config, message_config):
    global environment_config_local
    global message_config_local

    message_config_local = message_config
    environment_config_local = environment_config
