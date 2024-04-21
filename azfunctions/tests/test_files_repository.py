from uuid import UUID, uuid4
import pytest
from azure.cosmos import CosmosClient

# add project root to sys.path
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
# 
from shared.models import FileMetadataDb
from shared.files_repository import FilesRepository


@pytest.fixture
def repository():
    # Create a Cosmos DB client and initialize the repository
    client = CosmosClient(url="https://localhost:8081",
                credential=(
                    "C2y6yDjf5/R+ob0N8A7Cgv30VRDJIWEHLM+4QDU5DE2nQ9nDuVTqobD4b8mGGyPMbIZnqyMsEcaGQy67XIw/Jw=="
                ),)
    db_client = client.get_database_client("resumematchpro_test")
    return FilesRepository(db_client)


# add pytest fixture to delete all items from the container before each test
@pytest.fixture(autouse=True)
def run_around_tests(repository):
    repository.delete_all()
    
    
@pytest.fixture
def sample_CV() -> FileMetadataDb:
    return FileMetadataDb(
        user_id="b3f7b3b3-3b3b-3b3b-3b3b-3b3b3b3b3b3b",
        filename="cv.txt",
        type="CV",
        url="https://cv.com",
        text="Python Developer"
    )
    
def test_upsert_file(repository, sample_CV):
    # Create a sample file
    file = sample_CV

    # Add the file to the repository
    repository.upsert_file(file.model_dump(mode="json"))

    # Retrieve the file from the repository
    files = repository.get_files_from_db(user_id=file.user_id)
    assert len(files) == 1
    assert files[0].filename == file.filename
    
    
def test_upsert_file_empty_text(repository, sample_CV):
    # Create a sample file
    file = sample_CV
    file.text = None

    # Add the file to the repository
    repository.upsert_file(file.model_dump(mode="json"))

    # Retrieve the file from the repository
    files = repository.get_files_from_db(user_id=file.user_id)
    assert len(files) == 1
    assert files[0].filename == file.filename
    assert files[0].text == None
    
    
def test_get_files_from_db(repository, sample_CV):
    # Create a sample file
    file = sample_CV

    # Add the file to the repository
    repository.upsert_file(file.model_dump(mode="json"))

    # Retrieve the file from the repository
    files = repository.get_files_from_db(user_id=file.user_id)
    assert len(files) == 1
    assert files[0].filename == file.filename
    
    
def test_delete_file_by_user_id_and_filename(repository, sample_CV):
    # Create a sample file
    file = sample_CV

    # Add the file to the repository
    repository.upsert_file(file.model_dump(mode="json"))

    # Delete the file from the repository
    repository.delete_file(user_id=file.user_id, filename=file.filename)

    # Retrieve the file from the repository
    files = repository.get_files_from_db(user_id=file.user_id)
    assert len(files) == 0
    
# def test_delete_file_by_id(repository, sample_CV):
#     # Create a sample file
#     file = sample_CV

#     # Add the file to the repository
#     repository.upsert_file(file.model_dump(mode="json"))

#     # Retrieve the file from the repository
#     files = repository.get_files_from_db(user_id=file.user_id)
#     file_id = files[0].id
    
#     # Delete the file from the repository
#     repository.delete_file(file_id=file_id)

#     # Retrieve the file from the repository
#     files = repository.get_files_from_db(user_id=file.user_id)
#     assert len(files) == 0
    
    
def test_get_file_by_id(repository, sample_CV):
    # Create a sample file
    file = sample_CV

    # Add the file to the repository
    repository.upsert_file(file.model_dump(mode="json"))

    # Retrieve the file from the repository
    files = repository.get_files_from_db(user_id=file.user_id)
    file_id = files[0].id
    
    # Retrieve the file by ID
    file = repository.get_file_by_id(user_id=file.user_id, file_id=file_id)
    assert file.filename == sample_CV.filename
    assert file.id == file_id
    assert file.user_id == file.user_id
    assert file.type == file.type
    assert file.url == file.url
    assert file.text == file.text
    
def test_get_file_by_id_not_found(repository):
    # Retrieve the file by ID
    file = repository.get_file_by_id(user_id=uuid4(), file_id=uuid4())
    assert file is None