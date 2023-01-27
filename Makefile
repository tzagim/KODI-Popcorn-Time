ID := plugin.video.kodipopcorntime
VERSION := $(shell xmllint --xpath 'string(//addon/@version)' $(ID)/addon.xml)

all:
	git archive -o $(ID)-$(VERSION).zip HEAD $(ID)
