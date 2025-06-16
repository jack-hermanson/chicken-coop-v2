.PHONY: update-macros push-macros

update-macros:
	git submodule update --remote --merge
	git add application/web/templates/_macros
	git commit -m "Update macros to latest commit"

push-macros:
	cd application/web/templates/_macros && git push origin main
