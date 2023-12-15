import pytest
from playwright.sync_api import Page, expect

@pytest.mark.skip(reason="Used for older version of program")
def test_get_albums(page, test_web_address, db_connection):
    db_connection.seed("seeds/music_library.sql")
    page.goto(f"http://{test_web_address}/albums")
    div_tags = page.locator("div")
    expect(div_tags).to_have_text([
        "Title: Doolittle\nReleased: 1989",
        "Title: Nothing was the same\nReleased: 2013"
    ])

@pytest.mark.skip()
def test_single_album(page, test_web_address, db_connection):
    db_connection.seed("seeds/music_library.sql")
    page.goto(f"http://{test_web_address}/albums/1")
    heading = page.locator("h1")
    expect(heading).to_have_text("Doolittle")
    release_year = page.locator("div")
    expect(release_year).to_have_text("Released: 1989")

@pytest.mark.skip()
def test_get_artist_with_id(page, test_web_address, db_connection):
    db_connection.seed("seeds/artist_table.sql") 
    page.goto(f"http://{test_web_address}/artists/1")
    heading = page.locator("h1")
    expect(heading).to_have_text("Pixies")
    genre = page.locator("div")
    expect(genre).to_have_text("Genre: Rock")

@pytest.mark.skip()
def test_get_artists(page, test_web_address, db_connection):
    db_connection.seed("seeds/artist_table.sql") 
    page.goto(f"http://{test_web_address}/artists")
    links = page.locator("a")
    expect(links).to_have_text([
        "Pixies",
        "ABBA",
        "Taylor Swift",
        "Nina Simone",
        'Add Artist'
    ])
    page.screenshot(path="screenshot.png", full_page=False)