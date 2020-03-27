# 3rd
import os

from pathlib import Path as plPath  # Path
from os import path as osPath

# My
from crException import *
from crLogHeader import *
import crDevInput  # Information used while development

# Module scope config
magic_value_config_local = None
message_config_local = None

# Receive config


def init_environment(message_config, magic_value_config):
    global magic_value_config_local
    global message_config_local

    magic_value_config_local = magic_value_config
    message_config_local = message_config

# Create folder if not exist


def confirm_folder_exist(myFolder):
    folder_exist = False
    if osPath.exists(myFolder) is False:
        try:
            os.mkdir(myFolder)
            folder_exist = True
        except:
            error_message = message_config_local['err']['failed_to_create_output_folder']
            crPrintCyan(error_message)
            raise CrEnvironmentError(error_message)
    # else if myFolder already exist
    else:
        folder_exist = True

# Scan and get catalog file path


def get_catalog_chm_file_path():
    global magic_value_config_local
    global message_config_local

    catalog_file_path = None

    try:
        catalog_file_list = plPath(crDevInput.unpackedChmFolder) \
            .glob(magic_value_config_local['chm']['catalog_file_search_pattern'])
        catalog_file_list_count = 0

        for catalog_file in catalog_file_list:
            catalog_file_list_count = catalog_file_list_count + 1

            if catalog_file_list_count > 1:
                crPrintCyan(message_config_local['err']['multiple_catalog_file'])
                raise CrEnvironmentError(message_config_local['err']['multiple_catalog_file'])

            catalog_file_path = catalog_file

        if catalog_file_list_count is 0:
            # Nothing found, raise error
            error_message = message_config_local['err']['catalog_file_not_found']
            crPrintCyan(error_message)
            raise CrFileNotFoundError(error_message)
    except:
        raise

    return catalog_file_path

# Wrap the output folder with pathlib


def get_root_output_folder_full_path():
    output_folder = plPath(crDevInput.outputFolder)

    confirm_folder_exist(output_folder)

    return output_folder


# Combine serval information to catalog HTML full output path


def get_catalog_html_output_full_path(catalog_html_title):
    output_folder_path = get_root_output_folder_full_path()
    #
    # Catalog root node name  + `- Catalog` + `.html`
    output_file_path = output_folder_path.joinpath(
        catalog_html_title
        + message_config_local['html_catalog']['title']
        + magic_value_config_local['html']['file_extension'])

    return output_file_path

# Some entry need to preprocess before use


def get_preprocessed_environment(environment_config):
    # m = my
    mD = environment_config['data']
    mDC = environment_config['data_catalog_html_resource']

    # Copy data structure to output structure
    # Do this before preprocess data
    environment_config['output_catalog_html_resource'] = mDC

    # Generate full path for data_catalog files
    environment_config['data_catalog_html_resource']['css_file_full_path'] = mD['root_path'] + mDC['root_path'] + mDC['css_file_name']
    environment_config['data_catalog_html_resource']['js_file_full_path'] = mD['root_path'] + mDC['root_path'] + mDC['js_file_name']

    return environment_config
