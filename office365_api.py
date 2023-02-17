import environ
from office365.runtime.auth.user_credential import UserCredential
from office365.sharepoint.files.file import File
from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext

env = environ.Env()
environ.Env().read_env()

USERNAME = env('sharepoint_email')
PASSWORD = env('sharepoint_password')
SHAREPOINT_SITE = env('sharepoint_url_site')
SHAREPOINT_SITE_NAME = env('sharepoint_site_name')
SHAREPOINT_DOC = env('sharepoint_doc_library')
CLIENT_ID = env('client_id')
CLIENT_SECRET = env('client_secret')

class SharePoint:
    def _auth(self):
        ctx_auth = AuthenticationContext(SHAREPOINT_SITE)
        if ctx_auth.acquire_token_for_app(client_id=CLIENT_ID,
                                          client_secret=CLIENT_SECRET):
            conn = ClientContext(SHAREPOINT_SITE, ctx_auth)
            return conn
    
    def _get_files_list(self, folder_name):
        conn = self._auth()
        target_folder_url=f'{SHAREPOINT_DOC}/{folder_name}'
        root_folder = conn.web.get_folder_by_server_relative_url(target_folder_url)
        root_folder.expand(["Files","Folders"]).get().execute_query()
        return root_folder.files

    def download_file(self,file_name,folder_name):
        conn = self._auth()
        file_url = f'/sites/{SHAREPOINT_SITE_NAME}/{SHAREPOINT_DOC}/{folder_name}/{file_name}'
        file = File.open_binary(conn,file_url)
        return file.content

    def download_files(self,folder_name):
        return self._get_files_list(folder_name)
        
    

    
