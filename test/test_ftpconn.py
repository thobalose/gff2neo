"""
Testing ftpconn module
"""
import pytest

from tb2neo.ftpconn import get_nucleotides, download_fasta, FILE_PATH, \
    FASTA_FILE


def test_download_fasta_error():
    with pytest.raises(AttributeError):
        download_fasta(url=None, file_path=FILE_PATH, fasta_file=FASTA_FILE)


# def test_download_fasta():
#     result = download_fasta(url=URL, file_path=FILE_PATH,
#                             fasta_file=FASTA_FILE)
#     assert isinstance(result, GzipFile) is True


@pytest.mark.skip(reason="heavy on mem")
def test_get_nucleotides():
    result = get_nucleotides(strain="h37rv")
    assert isinstance(result, str) is True
