import datetime
import os
import shutil
import sys
# Save-repository location, relative to the user's home directory, for each
# platform. Kept as plain POSIX-style strings so they are platform-independent
# and can be joined correctly on any OS.
MACOS_SAVE_SUBPATH = (
    'Library',
    'Application Support',
    'unity.Failbetter Games.Sunless Skies',
    'storage',
    'characterrepository',
)
UNITY_DATA_SUBPATH = (
    'unity.Failbetter Games.Sunless Skies',
    'storage',
    'characterrepository',
)
WINDOWS_SAVE_SUBPATH = (
    'AppData', 'LocalLow', 'Failbetter Games', 'Sunless Skies',
    'storage', 'characterrepository',
)

# File-dialog filter shared by the Open/Save dialogs. The first entry is
# selected by default; ``autosave*.json`` matches every save flavour
# (``autosave.json``, ``autosave_backup.json`` and the legacy
# ``autosave_s.json`` / ``autosave_m.json`` names).
SAVE_FILE_FILTER = (
    'Save files (autosave*.json);;'
    'Autosave (autosave.json);;'
    'JSON Files (*.json);;'
    'All Files (*)'
)


def get_file_path(platform):
    # Return the default save-repository directory for the given platform.
    # `platform` is expected to be the value of `sys.platform`. Returns an
    # empty string when the location cannot be determined, so that callers
    # fall back to the current working directory instead of an invalid path.
    home = os.path.expanduser('~')

    if platform == 'win32':
        # Prefer the real user profile over %APPDATA% (which points one level
        # up inside the profile after dropping 'Roaming').
        profile = os.getenv('USERPROFILE') or home
        return os.path.join(profile, *WINDOWS_SAVE_SUBPATH)
    elif platform == 'darwin':
        return os.path.join(home, *MACOS_SAVE_SUBPATH)
    elif platform.startswith('linux'):
        # Unity stores saves under the XDG data home on Linux.
        data_home = os.getenv('XDG_DATA_HOME') or os.path.join(home, '.local', 'share')
        return os.path.join(data_home, *UNITY_DATA_SUBPATH)
    else:
        return ''


def get_display_name(file_name):
    # Return a short, human-readable name for a save file. Works with both
    # Windows (`\\`) and POSIX (`/`) separators, returning the last two path
    # components (e.g. `Lineage-6/autosave_s.json`).
    # Normalise both separators before splitting so mixed paths work too.
    normalized = file_name.replace('\\', '/').replace(os.sep, '/')
    parts = [part for part in normalized.split('/') if part]
    return os.sep.join(parts[-2:]) if parts else file_name
# File names that represent a complete save file, in preference order. The
# modern format is a single ``autosave.json``; older game versions stored the
# save as ``autosave_s.json`` alongside a metadata file.
SAVE_FILE_NAMES = ('autosave.json', 'autosave_s.json')


def find_latest_save(repository_path=None):
    # Return the path of the most recently modified full save file.
    #
    # Walks the character repository, which contains one ``Lineage-N`` folder
    # per character, and reports the freshest candidate (usually the save of the
    # current character). Files sitting directly in the repository root are
    # skipped: that copy is a trimmed summary without the full world/quality
    # data the editor needs. Returns ``None`` when nothing suitable is found or
    # the repository path is empty, so the caller can fall back to the dialog.
    root = repository_path or get_file_path(sys.platform)
    if not root or not os.path.isdir(root):
        return None
    candidates = []
    for base, _dirs, files in os.walk(root):
        # Only consider saves inside a character (Lineage) folder.
        if os.path.abspath(base) == os.path.abspath(root):
            continue
        for name in SAVE_FILE_NAMES:
            if name in files:
                full = os.path.join(base, name)
                try:
                    candidates.append((os.path.getmtime(full), full))
                except OSError:
                    pass
    if not candidates:
        return None
    return max(candidates)[1]


def backup_save_repository(repository_path):
    # Zip the whole character repository (every Lineage-N folder) into a
    # timestamped archive next to it, so a bad edit can always be undone.
    # Returns the path of the created .zip, or None if there's nothing to
    # back up.
    if not repository_path or not os.path.isdir(repository_path):
        return None

    parent = os.path.dirname(repository_path)
    folder_name = os.path.basename(repository_path)
    backups_root = os.path.join(parent, 'SaveEditorBackups')
    os.makedirs(backups_root, exist_ok=True)

    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    archive_base = os.path.join(backups_root, f'{folder_name}_backup_{timestamp}')

    return shutil.make_archive(archive_base, 'zip', root_dir=parent, base_dir=folder_name)
