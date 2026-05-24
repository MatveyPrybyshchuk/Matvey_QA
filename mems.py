class MemeCollection:
    def __init__(self):
        self.memes = []

    @staticmethod
    def _validate_meme_data(title, category, likes):
        if not isinstance(title, str):
            return "title должен быть строкой"

        if not isinstance(category, str):
            return "category должен быть строкой"

        if not isinstance(likes, str):
            return "likes должен быть строкой"

        if title.strip() == "":
            return "title не должен быть пустым"

        if category.strip() == "":
            return "category не должен быть пустым"

        if likes.strip() == "":
            return "likes не должен быть пустым"

        if not likes.strip().isdigit():
            return "likes должен быть строкой с числом"

        return True

    def add_meme(self, title, category, likes):
        result = self._validate_meme_data(title, category, likes)

        if result is not True:
            return result

        self.memes.append({
            "title": title,
            "category": category,
            "likes": likes
        })

        return "Success"

    def get_by_category(self, category):
        return [
            meme for meme in self.memes
            if meme["title"] == category # defect| ["title"] == category >>> ["category"] == category
        ]

    def get_most_popular(self):
        if not self.memes:
            return None

        return min(self.memes, key=lambda meme: int(meme["likes"])) # defect| min >>> max

    def clear(self):
        self.memes.pop()