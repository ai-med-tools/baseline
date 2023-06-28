import pytest
from baseline.essay.meta import Meta


class TestMeta:
    def test_init_correct(self, meta_dict_correct):
        meta_operand = meta_dict_correct
        meta = Meta(meta_operand)
        assert(meta.id == meta_operand['id'])

    def test_init_incorrect(self, meta_dict_incorrect):
        with pytest.raises(TypeError):
            meta_operand = meta_dict_incorrect
            Meta(meta_operand)

