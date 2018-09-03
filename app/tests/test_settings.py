import pytest
import sys
sys.path.append("/home/dsteffen/python/wiki/app")

from settings import Settings

tree = {
	"python": {
		"path": ".",
		"title": "Python Cheat Sheet",
		"subpages": None
	},
	"ansible": {
		"path": ".",
		"title": "Ansible eine Kurz-Uebersicht",
		"subpages": {
			"vault": {
				"path": "ansible/vault",
				"title": "Ansible Vault",
				"subpages": {
                                    "example":
                                        {
                                            "path": "ansible/vault/beispiel",
                                            "title": "Ansible-Vault-Beispiel",
                                            "subpages": None
                                        }
                                    }
			}
		}
	}
}

rs = Settings()

def test_readConfig():
    assert rs.readConfig() == tree