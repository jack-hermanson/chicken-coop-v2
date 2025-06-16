.PHONY: update-macros push-macros

update-macros:
	git submodule update --remote --merge
	git add shared_macros
	git commit -m "Update shared_macros to latest commit"

push-macros:
	cd shared_macros && git push origin main
