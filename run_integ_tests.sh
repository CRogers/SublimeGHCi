SUBLIME_DIR=''

if [ "$(uname)" == "Darwin" ]; then
    SUBLIME_DIR="$HOME/Library/Application Support/Sublime Text 3"
elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
	SUBLIME_DIR="$HOME/.config/sublime-text-3"
else
	echo Can\'t detect OS
	exit 1
fi

SUBLIME_USER_SETTINGS="$SUBLIME_DIR/Packages/User/Preferences.sublime-settings"
SUBLIME_USER_SETTINGS_BAK="$SUBLIME_USER_SETTINGS.bak"
mv "$SUBLIME_USER_SETTINGS" "$SUBLIME_USER_SETTINGS_BAK"
mv IntegTests.sublime-settings.sample "$SUBLIME_USER_SETTINGS"

python3 -m unittest discover -c -s integ_tests -p *IntegSpec.py
EXIT_STATUS=$?

mv "$SUBLIME_USER_SETTINGS_BAK" "$SUBLIME_USER_SETTINGS"

exit $EXIT_STATUS
