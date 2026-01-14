import zipfile
from pathlib import Path

from functions.backup_mail_folder import backup_folder



def test_backup_folder_creates_zip(tmp_path, monkeypatch):
    # Arrange
    source_folder = tmp_path / "mail_folder"
    source_folder.mkdir()

    # Create files in the mail folder
    file1 = source_folder / "test1.txt"
    file2 = source_folder / "sub" / "test2.txt"
    file2.parent.mkdir()

    file1.write_text("hello")
    file2.write_text("world")

    # Run in temp dir so mail_folder_backups is created there
    monkeypatch.chdir(tmp_path)

    cfg = {
        "backup_zip_file_compr_level": "6"
    }

    # Act
    zip_path = backup_folder(str(source_folder), cfg)

    # Assert: ZIP exists
    zip_path = Path(zip_path)
    assert zip_path.exists()
    assert zip_path.suffix == ".zip"

    # Assert: ZIP contains expected files
    with zipfile.ZipFile(zip_path, "r") as zipf:
        names = zipf.namelist()

    assert "test1.txt" in names
    assert "sub/test2.txt" in names or "sub\\test2.txt" in names