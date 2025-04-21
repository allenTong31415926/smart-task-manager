import pytest
from tags.utils import extract_tags_from_title

@pytest.mark.django_db
class TestTagUtils:
    def test_extract_tags_from_title_single_match(self):
        title = 'Task with urgent deadline'
        tags = extract_tags_from_title(title)
        assert len(tags) == 1
        assert 'urgent' in tags

    def test_extract_tags_from_title_multiple_matches(self):
        title = 'Urgent bug fix needed for UI design'
        tags = extract_tags_from_title(title)
        assert len(tags) == 3
        assert 'urgent' in tags
        assert 'bug' in tags
        assert 'design' in tags

    def test_extract_tags_from_title_no_matches(self):
        title = 'Regular task without any special keywords'
        tags = extract_tags_from_title(title)
        assert len(tags) == 0

    def test_extract_tags_from_title_case_insensitive(self):
        title = 'URGENT task with Bug and DESIGN'
        tags = extract_tags_from_title(title)
        assert len(tags) == 3
        assert 'urgent' in tags
        assert 'bug' in tags
        assert 'design' in tags 