import urllib.parse
import json
import logging
import os
import zipfile
from urllib.parse import urljoin
import requests


from app.core.config import settings


log = logging.getLogger(__name__)



class GeoAPI:
    def __init__(
        self,
        url: str = settings.GEOSERVER_URL,
        id_: str = settings.GEOSERVER_ID,
        pw: str = settings.GEOSERVER_PASSWORD
    ):
        self.url = url
        self.headers = {"content-type": "application/json"}
        self.auth = (id_, pw)

    def _file_to_zip(self, filePath: str) -> str:
        """파일을 zip 파일로 압축 및 해당 경로 리턴"""
        filePath = os.path.abspath(filePath)
        basename = os.path.basename(filePath)
        dir_name = os.path.dirname(filePath)
        name, _, _ = basename.rpartition(".")

        zip_path = os.path.join(dir_name, f"{name}.zip")
        zip_file = zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED)
        zip_file.write(filePath, basename)
        zip_file.close()

        return zip_path

    def workspaces_get(self) -> list[dict[str, str]]:
        """workspace 정보 조회"""
        resource = "workspaces"
        url = urljoin(self.url, resource)
        resp = requests.get(url, headers=self.headers, auth=self.auth)
        resp.raise_for_status()

        resp_json = resp.json()["workspaces"]
        return resp_json["workspace"] if resp_json else []

    def workspaces_create(self, name: str) -> bool:
        """workspace 생성"""
        resource = "workspaces"
        url = urljoin(self.url, resource)

        payload = {"workspace": {"name": name}}
        resp = requests.post(
            url, auth=self.auth, headers=self.headers, data=json.dumps(payload)
        )
        resp.raise_for_status()

        return True

    def coveragestoresGet(self, workspace: str) -> list[dict[str, str]]:
        """coverage 정보 조회"""
        resource = f"workspaces/{workspace}/coveragestores"
        url = urljoin(self.url, resource)

        resp = requests.get(url, headers=self.headers, auth=self.auth)
        resp.raise_for_status()

        coverage_stores = resp.json().get('coverageStores')

        coverage_store = []

        if coverage_stores:
            coverage_store = coverage_stores.get('coverageStore')

        return coverage_store

    def datastoreForShpCreate(self, workspace, datastoreName, files):

        resource = f"workspaces/{workspace}/datastores/{datastoreName}/file.shp"
        params = {"charset": "EUC-KR"}
        queryParams = urllib.parse.urlencode(params)
        url = urljoin(self.url, resource)
        url += "?" + queryParams
        url.encode('utf-8')
        headers = {
            'Content-type': 'application/zip',
        }
        with open(files, 'rb') as file:

            response = requests.put(
                url,
                auth=self.auth,
                headers=headers,
                data=file
            )

        return response

    def layerGroupCreate(self, workspaceName: str,
                         layerList: list, layerGroupName: str):

        headers = {"Content-Type": "application/json"}

        payload = {
            "layerGroup": {
                "name": layerGroupName,
                "mode": "SINGLE",
                # "bounds": {
                #     "crs": "EPSG:4326",
                #     "minx": "-180",
                #     "miny": "-180",
                #     "maxx": "180",
                #     "maxy": "180",
                # },
                "layers": {
                    "layer": [
                        {"name": layerName}
                        for layerName in layerList
                    ]
                }
            }
        }
        resource = f"workspaces/{workspaceName}/layergroups"

        url = urljoin(self.url, resource)
        response = requests.post(
            url,
            data=json.dumps(payload),
            headers=headers,
            auth=self.auth
        )

        return response
