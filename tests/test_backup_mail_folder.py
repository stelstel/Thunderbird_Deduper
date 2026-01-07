import os
import zipfile
from functions.backup_mail_folder import backup_folder



def test_backup_folder_creates_zip(tmp_path, monkeypatch):
    # Arrange: create a fake mail folder
    source_folder = tmp_path / "mail_folder"
    source_folder.mkdir()

    test_file = source_folder / "test.txt"
    test_file.write_text("hello thunderbird")

    # Run backups in temp directory instead of project root
    monkeypatch.chdir(tmp_path)

    # Act
    zip_path = backup_folder(str(source_folder))

    # Assert: zip file exists
    assert os.path.exists(zip_path)

    # Assert: zip contains the file
    with zipfile.ZipFile(zip_path, "r") as z:
        names = z.namelist()
        assert "test.txt" in [os.path.basename(n) for n in names]
