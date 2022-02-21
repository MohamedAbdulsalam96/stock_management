from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in stock_management/__init__.py
from stock_management import __version__ as version

setup(
	name="stock_management",
	version=version,
	description="Manage stock and stock movement.",
	author="Rahib Hassan",
	author_email="rahib@frappe.io",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
