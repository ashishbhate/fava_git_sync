export default {
  guessURL() {
	const re = /^(.*)\/(?:income_statement|balance_sheet|trial_balance|journal|query|holdings|commodities|documents|events|statstics|editor|import|options|help)\/?$/;
	const url = window.location.href
	const found = url.match(re)
	if (!found) {
		return "/beancount"
	}
	return found[1]
  },

  guessedURL: "",

  init() {   
	this.guessedURL = this.guessURL()
	const spacer = document.querySelector("header > span.spacer"); 
	const header = document.querySelector("header"); 

	const syncButton = document.createElement("Button");
	syncButton.id = "git-sync-button"
	syncButton.textContent = 'sync'
	syncButton.style.fontWeight = "bold"
	syncButton.style.cursor = "pointer"

	var timeout
	syncButton.onclick = async () => {
		clearTimeout(timeout)
		fetch(this.guessedURL + "/extension/FavaGitSync/sync").
			then(response => {
				if (response.ok) {
					syncButton.textContent = "sync ✅"
					syncButton.style.backgroundColor = ""
					timeout = setTimeout(() => {syncButton.textContent = "sync"}, 2000)
					syncButton.blur()
				} else {
					syncButton.textContent = "sync fail"
					syncButton.style.backgroundColor = "red"
					syncButton.blur()
				}
			})
	}

	header.insertBefore(syncButton, spacer)
  },
  onPageLoad() {
	const syncButton = document.getElementById("git-sync-button");
	if (syncButton == null) {
		return
	}
	fetch(this.guessedURL + "/extension/FavaGitSync/status").
		then(response => {
			if (response.status == 250) {
				syncButton.textContent = "sync 🟠"
			} else if (response.status == 200) {

			} else {
				syncButton.textContent = "sync ?"
			}
		})
  },
  onExtensionPageLoad() {
  },
};