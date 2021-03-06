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


def crCreateFolder(myFolder):
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

# Search in input folder and get catalog file path


def get_catalog_chm_file_full_path():
    global magic_value_config_local
    global message_config_local

    # Result placeholder
    catalog_file_full_path = None

    try:
        # Glob all potential catalog file
        # Call it a list, but see python generator for more information
        catalog_file_list = plPath(crDevInput.unpackedChmFolder) \
            .glob(magic_value_config_local['chm']['catalog_file_search_pattern'])

        # Expect only one catalog file
        catalog_file_list_count = 0

        # Explore the glob generator
        for catalog_file_glob_result in catalog_file_list:
            # Increase file count on every loop
            catalog_file_list_count = catalog_file_list_count + 1

            # Prevent more than one catalog file
            if catalog_file_list_count > 1:
                crPrintCyan(message_config_local['err']['multiple_catalog_file'])
                raise CrNotImplementedError(message_config_local['err']['multiple_catalog_file'])

            # Everything is fine, copy it as plPath
            catalog_file_full_path = plPath(catalog_file_glob_result)

        # After explored the generator
        if catalog_file_list_count is 0:
            # Nothing found, raise error
            error_message = message_config_local['err']['catalog_file_not_found']
            crPrintCyan(error_message)
            raise CrFileNotFoundError(error_message)
    except:
        raise

    return catalog_file_full_path

# get_root_output_folder_full_path


def get_root_output_folder_full_path():
    output_folder = plPath(crDevInput.outputFolder)

    crCreateFolder(output_folder)

    return output_folder


# Combine serval information to generate catalog HTML full output path


def get_catalog_html_output_full_path(catalog_html_title):
    output_folder_path = get_root_output_folder_full_path()
    #
    # Catalog root node name  + `- Catalog` + `.html`
    output_file_path = output_folder_path.joinpath(
        catalog_html_title
        + message_config_local['html_catalog']['title']
        + magic_value_config_local['html']['file_extension'])

    return output_file_path

# get_preprocessed_environment


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
