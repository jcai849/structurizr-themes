all: aws-theme.json azure-theme.json

azure-theme.json:
	./theme-png-cache.py https://static.structurizr.com/themes/microsoft-azure-2023.01.24/ >$@

aws-theme.json:
	./theme-png-cache.py https://static.structurizr.com/themes/amazon-web-services-2022.04.30/ >$@