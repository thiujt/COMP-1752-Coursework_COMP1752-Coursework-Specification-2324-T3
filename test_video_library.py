from video_library import LibraryItem

def test_library_item_creation():
    # The correct order should be: video_number, name, director, rating, play_count, image_path, media_path
    item = LibraryItem("01", "Thien Ly Oi", "J97", 4, 0, "csv/thien_ly_oi.jpg", "csv/thien_ly_oi.mp3")
    assert item.get_name() == "Thien Ly Oi"
    assert item.get_director() == "J97"
    assert item.get_rating() == 4
    assert item.get_play_count() == 0
    assert item.get_image_path() == "csv/thien_ly_oi.jpg"
    assert item.get_media_path() == "csv/thien_ly_oi.mp3"

def test_set_rating():
    item = LibraryItem("02", "Tam Ka", "Wrxdie", 2, 0, "csv/tam_ka.jpg", "csv/tam_ka.mp3")
    item.set_rating(5)
    assert item.get_rating() == 5

def test_increment_play_count():
    item = LibraryItem("03", "Che Ho", "Wrxdie", 3, 0, "csv/che_ho.mp3", "csv/che_ho.mp3")
    item.increment_play_count()
    assert item.get_play_count() == 1
