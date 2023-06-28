import setuptools

setuptools.setup(
	name="baseline",
	version="0.0.8",
	author="Webpractik",
	author_email="kai@webpractik.ru, pk@webpractik.com",
	description="Baseline конкурса Read//able для участников",
	url="https://github.com/webpractik/python-psr",
	packages=setuptools.find_packages(include=['baseline', 'baseline.*']),
	classifiers=[
		"Programming Language :: Python :: 3.10",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.10',
	# py_modules=["baseline.cli"],
	include_package_data=True,
	install_requires=[
		"aiohttp",
		"click",
		"loguru",
		"jsonschema",
		# "python-socketio[asyncio-client]"
	],
# 	entry_points="""
# 		[console_scripts]
# 		baseline=baseline.cli:cli
# 	""",
)
