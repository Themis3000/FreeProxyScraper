import requests
from utils.plugins import Proxy, Plugin
from typing import Iterator


anon_dict = {"transparent": 0, "anonymous": 1, "elite": 2}


class GeoNode(Plugin):
    # Disabled because the website almost always lies about the anominity of proxies
    enabled = False
    plugin_name = "Geonode"
    plugin_url = "https://geonode.com/free-proxy-list"

    def find(self) -> Iterator[Proxy]:
        page = 1
        while True:
            resource = f"https://proxylist.geonode.com/api/proxy-list?limit=15&page={page}&sort_by=lastChecked&sort_type=desc"
            response = requests.get(resource)

            if response.status_code != 200:
                self.report_fail()
                return

            response_json = response.json()

            if len(response_json["data"]) == 0:
                return

            for proxy_json in response_json["data"]:
                yield Proxy(
                    ip=proxy_json["ip"],
                    anon_level=anon_dict[proxy_json["anonymityLevel"]],
                    port=int(proxy_json["port"]),
                    protocol=proxy_json["protocols"][0]
                )

            page += 1
