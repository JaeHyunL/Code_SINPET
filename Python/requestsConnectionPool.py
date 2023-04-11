            sess = requests.Session()
            adapter = requests.adapters.HTTPAdapter(pool_connections=100, pool_maxsize=100)
            sess.mount('http://', adapter)
            response = sess.put(
                url,
                auth=self.auth,
                headers=headers,
                data=file
            )
