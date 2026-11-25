"""Git clean/smudge filter that keeps the private OneDrive URL out of the repository.

The Power BI FilePath parameter points to the fuel log in OneDrive for Business.
That URL contains the tenant and user name, so it must not be committed.

- clean  (runs on `git add`):  real URL  -> placeholder
- smudge (runs on checkout):   placeholder -> real URL

The real URL lives only in the local git config (never pushed):

    git config fuel.sourceUrl "https://<tenant>-my.sharepoint.com/personal/<user>/Documents/.../fuel-log.xlsx"

If fuel.sourceUrl is not set, the filter passes content through unchanged.
.gitattributes assigns the filter to expressions.tmdl; the commands are registered
per clone (local config, not versioned):

    git config filter.sourceurl.clean  "python -I tools/source_url_filter.py clean"
    git config filter.sourceurl.smudge "python -I tools/source_url_filter.py smudge"
"""
import subprocess
import sys

PLACEHOLDER = "https://YOUR-TENANT-my.sharepoint.com/personal/YOUR_USER/Documents/fuel-log.xlsx"


def main() -> None:
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    data = sys.stdin.buffer.read()
    url = subprocess.run(["git", "config", "--get", "fuel.sourceUrl"],
                         capture_output=True, text=True).stdout.strip()
    if url and mode in ("clean", "smudge"):
        old, new = (url, PLACEHOLDER) if mode == "clean" else (PLACEHOLDER, url)
        data = data.replace(old.encode("utf-8"), new.encode("utf-8"))
    sys.stdout.buffer.write(data)


if __name__ == "__main__":
    main()
