import pytest
from mems import MemeCollection




class TestMemesCollection:
    """1. Создайте фикстуры"""

    """Фикстура, которая создаёт и возвращает пустую коллекцию мемов."""
    @pytest.fixture
    def create_empty_collections(self) -> MemeCollection:
        return MemeCollection()

    """Фикстура, которая создаёт коллекцию и заранее добавляет в неё несколько мемов."""
    @pytest.fixture
    def create_not_empty_collections(self, ) -> MemeCollection:
        memes = MemeCollection()
        memes.add_meme(title = "title", category = "category", likes = 10)
        return memes

    """Фикстура, которая очищает коллекцию после прохождения теста."""
    @pytest.fixture
    def clear_collections(self, create_not_empty_collections) -> MemeCollection:
        yield create_not_empty_collections
        create_not_empty_collections.clear()


    """2. Проверьте базовое поведение коллекции"""

    def test_empty_memes(self, create_empty_collections):
        """новая коллекция мемов пустая"""
        collection = create_empty_collections
        
        assert len(collection.memes) == 0


    def test_filled_memes(self, create_not_empty_collections):
        """подготовленная через фикстуру коллекция содержит мемы;"""
        collection = create_not_empty_collections

        assert len(collection.memes) > 0


    def test_succ_upload(self, create_empty_collections):
        """новый мем успешно добавляется в коллекцию"""
        collection = create_empty_collections

        collection.add_meme(title = "title_2", category = "category_2", likes = 10)
        result = collection.get_by_category("category_2")

        assert len(result) > 0



    def test_len_is_updated(self, create_not_empty_collections):
        """после добавления количество мемов увеличивается на 1"""
        collection = create_not_empty_collections

        len_before = len(collection.memes)
        collection.add_meme(title = "title_2", category = "category_2", likes = 10)
        len_after = len(collection.memes)

        assert len_after > len_before


    def test_added_data(self, create_empty_collections):
        """данные добавленного мема сохраняются корректно: title, category, likes."""
        collection = create_empty_collections
        
        collection.add_meme(title = "title_3", category = "category_3", likes = 100)
        result = collection.get_by_category("category_3")

        assert result[0]["title"] == "title_3"
        assert result[0]["category"] == "category_3"
        assert result[0]["likes"] == 100


    """3. Проверьте поиск по категории"""

    def test_category_exist(self, create_not_empty_collections):
        """Категория существует — метод возвращает список мемов этой категории."""
        collection = create_not_empty_collections
        result = collection.get_by_category("category")
        assert len(result) > 0


    def test_category_not_exist(self, create_not_empty_collections):
        """Категория не существует — метод возвращает пустой список."""
        collection = create_not_empty_collections
        result = collection.get_by_category("category__")
        assert len(result) == 0


    """4. Проверьте поиск самого популярного мема"""

    def test_likes_empty_collection(self, create_empty_collections):
        """в коллекции нет мемов — метод возвращает None"""
        collection = create_empty_collections
        result = collection.get_most_popular()
        assert result is None


    def test_likes_filled_collection(self, create_empty_collections):
        """в коллекции несколько мемов c разным количеством лайков — метод возвращает мем c максимальным количеством лайков"""
        collection = create_empty_collections
        collection.add_meme(title = "title_1", category = "category_1", likes = 100)
        collection.add_meme(title = "title_2", category = "category_1", likes = 150)
        collection.add_meme(title = "title_3", category = "category_2", likes = 140)
        result = collection.get_most_popular()
        assert result["title"] == "title_2"
        assert result["category"] == "category_1"
        assert result["likes"] == 150


    def test_likes_same_num_likes_collection(self, create_empty_collections):
        """в коллекции несколько мемов с одинаковым количеством лайков — метод возвращает один из мемов с этим значением."""
        collection = create_empty_collections
        collection.add_meme(title = "title_1", category = "category_1", likes = 100)
        collection.add_meme(title = "title_2", category = "category_1", likes = 150)
        collection.add_meme(title = "title_3", category = "category_2", likes = 150)
        result = collection.get_most_popular()
        assert result["title"] in ["title_2", "title_3"]
        assert result["category"] in ["category_1", "category_2"]
        assert result["likes"] in [150]


    """5. Проверьте очистку коллекции"""

    def test_clear_fixture(self, create_not_empty_collections):
        """Проверьте очистку коллекции"""
        collection = create_not_empty_collections
        assert len(collection.memes) > 0
        collection.clear()
        assert len(collection.memes) == 0


    """6. Проверьте валидацию входных данных"""

    @pytest.mark.parametrize("title, category, likes, expected_num", [
        ("mem", "category", "1", 1), # POS: title должен быть строкой
        (2, "category", "1", 0),     # NEG: title должен быть строкой
        ("mem", "category", "1", 1), # POS: category  должен быть строкой
        ("mem", 2, "1", 0),          # NEG: category  должен быть строкой
        ("mem", "category", 6, 1),   # POS: likes должен быть числом;
        ("mem", "category", "1", 0), # NEG: likes должен быть числом;

        ("mem", "category", "1", 1), # POS: title не должен быть пустым;
        ("", "category", "1", 0),    # NEG: title не должен быть пустым;
        ("mem", "category", "1", 1), # POS: category не должен быть пустым;
        ("mem", "", "1", 0),         # NEG: category не должен быть пустым;
        ("mem", "category", 0, 1),   # POS: likes не должен быть отрицательным;
        ("mem", "category", -1, 0),  # NEG: likes не должен быть отрицательным;
        ("mem", "category", 1, 1),   # NEG: likes не должен быть отрицательным;
    ])
    def test_data_acceptance(self, create_empty_collections, title, category, likes, expected_num):
        """Проверьте валидацию входных данных"""
        collection = create_empty_collections

        collection.add_meme(title, category, likes)
        assert len(collection.memes) == expected_num  
