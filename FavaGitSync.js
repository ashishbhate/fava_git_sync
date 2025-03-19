export default {
  guessURL() {
    const re =
      /^(.*)\/(?:income_statement|balance_sheet|trial_balance|journal|query|holdings|commodities|documents|events|statstics|editor|import|options|help)\/?$/;
    const url = window.location.href;
    const found = url.match(re);
    if (!found) {
      return "/beancount";
    }
    return found[1];
  },

  guessedURL: "",

  init() {
    this.guessedURL = this.guessURL();
    this.remoteAheadCount = 0;
    this.syncStatus = "";
    const spacer = document.querySelector("header > span.spacer");
    const header = document.querySelector("header");

    const syncButton = document.createElement("Button");
    syncButton.id = "git-sync-button";
    syncButton.textContent = "sync";
    syncButton.style.fontWeight = "bold";
    syncButton.style.cursor = "pointer";

    var timeout;
    syncButton.onclick = async () => {
      clearTimeout(timeout);
      fetch(this.guessedURL + "/extension/FavaGitSync/sync").then(
        (response) => {
          if (response.ok) {
            this.syncStatus = "✅";
            this.remoteAheadCount = "0";
            this.setButtonText();
            // syncButton.textContent = "sync ✅";
            syncButton.style.backgroundColor = "";
            timeout = setTimeout(() => {
              // syncButton.textContent = "sync";
              this.syncStatus = "";
              this.setButtonText();
            }, 2000);
            syncButton.blur();
          } else {
            // syncButton.textContent = "sync fail";
            this.syncStatus = "fail";
            this.setButtonText();
            syncButton.style.backgroundColor = "red";
            syncButton.blur();
          }
        }
      );
    };

    header.insertBefore(syncButton, spacer);
  },

  onPageLoad() {
    const syncButton = document.getElementById("git-sync-button");
    if (syncButton == null) {
      return;
    }
    fetch(this.guessedURL + "/extension/FavaGitSync/status").then(
      (response) => {
        if (response.status == 250) {
          response.text().then((aheadCount) => {
            if (aheadCount != "") {
              this.remoteAheadCount = aheadCount;
            }
            this.syncStatus = "🟠";
            this.setButtonText();
          });
        } else if (response.status == 200) {
          response.text().then((aheadCount) => {
            if (aheadCount != "") {
              this.remoteAheadCount = aheadCount;
            }
            this.setButtonText();
          });
        } else {
          this.syncStatus = "?";
          this.setButtonText();
        }
      }
    );
  },

  setButtonText() {
    const syncButton = document.getElementById("git-sync-button");
    if (syncButton == null) {
      return;
    }
    console.log("I AM SETTING BUTTON TEXT");
    var text = `sync ${this.syncStatus}`;
    if (this.remoteAheadCount != "" && this.remoteAheadCount != "0") {
      text = `${text} [${this.remoteAheadCount}]`;
    }
    syncButton.textContent = text;
  },

  onExtensionPageLoad() {},
};
