server_name = 'czcetin.sharepoint.com'
site_name = 'APD'
site_rel_path = '/sites/' + site_name
site_abs_path = 'https://' + server_name + site_rel_path
folder_root_rel_path = site_rel_path + '/Dokumenty'
folder_root_abs_path = 'https://' + server_name + folder_root_rel_path

config_cert = {
    'app_id'       : 'd2fcf993-929b-4c32-a235-a7ba643d4338',\
    'apd_site_id'  : 'czcetin.sharepoint.com,4bbd7b7f-7b70-40ef-9ab6-a9cb0e60997f,932264d4-30cc-42fd-878b-9b0d8d86d948',\
    'pfx_path'     : 'apd_self_signed.pfx',\
    'pfx_password' : 'nechutne21DlouheHeslo',\
}

config = {\
	'username'             : 'x0561517@cetin.cz',\
	'password'             : 'Kozlos18Kozlos18',\
        'server_name'          : server_name,\
	'site_name'            : site_name,\
	'site_rel_path'        : site_rel_path,\
	'site_abs_path'        : site_abs_path,\
	'folder_root_rel_path' : folder_root_rel_path,\
	'folder_root_abs_path' : folder_root_abs_path
}
