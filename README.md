# excel_inventory

# install python3
sudo yum install -y https://centos7.iuscommunity.org/ius-release.rpm  
sudo yum install python36u python36u-libs python36u-devel python36u-pip  
sudo pip3.6 install openpyxl  
sudo pip3.6 install pyyaml

  $ ./excel_inventory.py | python -m json.tool
  {
      "_meta": {
          "hostvars": {
              "haproxy001": {
                  "ansible_host": "192.168.0.5",
                  "frontend_ip": "10.100.0.1",
                  "frontend_port": 80
              },
              "haproxy011": {
                  "ansible_host": "192.168.0.14",
                  "frontend_ip": "10.100.1.1",
                  "frontend_port": 80
              },
              "webserver001": {
                  "ansible_host": "192.168.0.1",
                  "is_backup": false,
                  "web_ip": "10.0.0.1",
                  "web_port": 8080,
                  "weight": 1
              },
              "webserver002": {
                  "ansible_host": "192.168.0.2",
                  "is_backup": false,
                  "web_ip": "10.0.0.2",
                  "weight": 2
              },
              "webserver003": {
                  "ansible_host": "192.168.0.3",
                  "is_backup": false,
                  "web_ip": "10.0.0.3",
                  "weight": 3
              },
              "webserver004": {
                  "ansible_host": "192.168.0.4",
                  "is_backup": true,
                  "web_ip": "10.0.0.4"
              },
              "webserver011": {
                  "ansible_host": "192.168.0.11",
                  "is_backup": false,
                  "web_ip": "10.0.1.1",
                  "weight": 1
              },
              "webserver012": {
                  "ansible_host": "192.168.0.12",
                  "is_backup": false,
                  "web_ip": "10.0.1.2",
                  "weight": 3
              },
              "webserver013": {
                  "ansible_host": "192.168.0.13",
                  "is_backup": false,
                  "web_ip": "10.0.1.3",
                  "weight": 5
              }
          }
      },
      "all": {
          "vars": {
              "all_test1": 123234,
              "all_test2": 2.13,
              "all_test3": true,
              "all_test4": "test_data"
          }
      },
      "cluster001": {
          "hosts": [
              "webserver001",
              "webserver002",
              "webserver003",
              "webserver004",
              "haproxy001"
          ]
      },
      "cluster002": {
          "hosts": [
              "webserver011",
              "webserver012",
              "webserver013",
              "haproxy011"
          ]
      },
      "haproxy": {
          "hosts": [
              "haproxy001",
              "haproxy011"
          ],
          "vars": {
              "frontend_port": 80,
              "ha_proxy_conf_path": "/etc/haproxy/haproxy.cfg"
          }
      },
      "web001": {
          "hosts": [
              "webserver001",
              "webserver002",
              "webserver003",
              "webserver004",
                "haproxy001"
          ]
      },
      "web002": {
          "hosts": [
              "webserver011",
              "webserver012",
              "webserver013",
              "haproxy011"
          ]
      },
      "webservers": {
          "hosts": [
              "webserver001",
              "webserver002",
              "webserver003",
              "webserver004",
              "webserver011",
              "webserver012",
              "webserver013"
          ],
          "vars": {
              "web_conf_path": "/etc/httpd/conf/httpd.conf",
              "web_port": 80
          }
      }
  }
   
